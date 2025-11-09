from flask import Blueprint, render_template, jsonify, request
from app.database.session import Session
from app.database import crud
from app.tasks.job_scraper import JobScraper
from app.tasks.content_generator import ContentGenerationTask
from app.core.constants import JOB_STATUS
from app.utils.logger import get_logger

logger = get_logger(__name__)

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('dashboard.html')

@main_bp.route('/api/jobs')
def get_jobs():
    db = Session()
    try:
        status = request.args.get('status')
        skip = int(request.args.get('skip', 0))
        limit = int(request.args.get('limit', 50))
        
        if status:
            jobs = crud.get_jobs_by_status(db, status)
        else:
            jobs = crud.get_all_jobs(db, skip=skip, limit=limit)
        
        jobs_data = [
            {
                'id': job.id,
                'job_id': job.job_id,
                'title': job.title,
                'description': job.description[:200] + '...' if len(job.description) > 200 else job.description,
                'category': job.category,
                'budget': job.budget,
                'complexity': job.complexity,
                'status': job.status,
                'platform': job.platform,
                'url': job.url,
                'created_at': job.created_at.isoformat() if job.created_at else None
            }
            for job in jobs
        ]
        
        return jsonify({'jobs': jobs_data, 'count': len(jobs_data)})
    finally:
        db.close()

@main_bp.route('/api/jobs/<job_id>/content')
def get_job_content(job_id):
    db = Session()
    try:
        contents = crud.get_content_by_job_id(db, job_id)
        
        content_data = [
            {
                'id': content.id,
                'content_type': content.content_type,
                'generated_text': content.generated_text,
                'created_at': content.created_at.isoformat() if content.created_at else None
            }
            for content in contents
        ]
        
        return jsonify({'content': content_data})
    finally:
        db.close()

@main_bp.route('/api/scrape', methods=['POST'])
def trigger_scrape():
    try:
        scraper = JobScraper()
        result = scraper.run()
        return jsonify(result)
    except Exception as e:
        logger.error(f"Error in manual scraping: {e}")
        return jsonify({'status': 'error', 'error': str(e)}), 500

@main_bp.route('/api/generate/<job_id>', methods=['POST'])
def trigger_generation(job_id):
    try:
        generator = ContentGenerationTask()
        success = generator.generate_for_job(job_id)
        
        if success:
            return jsonify({'status': 'success', 'job_id': job_id})
        else:
            return jsonify({'status': 'error', 'message': 'Generation failed'}), 500
    except Exception as e:
        logger.error(f"Error in manual generation: {e}")
        return jsonify({'status': 'error', 'error': str(e)}), 500

@main_bp.route('/api/stats')
def get_stats():
    db = Session()
    try:
        all_jobs = crud.get_all_jobs(db)
        
        stats = {
            'total_jobs': len(all_jobs),
            'pending': len([j for j in all_jobs if j.status == JOB_STATUS['PENDING']]),
            'in_progress': len([j for j in all_jobs if j.status == JOB_STATUS['IN_PROGRESS']]),
            'completed': len([j for j in all_jobs if j.status == JOB_STATUS['COMPLETED']]),
            'failed': len([j for j in all_jobs if j.status == JOB_STATUS['FAILED']])
        }
        
        return jsonify(stats)
    finally:
        db.close()

@main_bp.route('/proposals')
def proposals_page():
    return render_template('proposals.html')

@main_bp.route('/settings')
def settings_page():
    return render_template('settings.html')

@main_bp.route('/api/proposals/<job_id>', methods=['POST'])
def generate_proposal(job_id):
    try:
        from app.ai.proposal_generator import ProposalGenerator
        from app.database.models import Proposal
        
        db = Session()
        try:
            job = crud.get_job_by_id(db, job_id)
            if not job:
                return jsonify({'status': 'error', 'message': 'Job not found'}), 404
            
            data = request.get_json() or {}
            proposal_type = data.get('type', 'standard')
            
            generator = ProposalGenerator()
            
            if proposal_type == 'short':
                proposal_text = generator.generate_short_proposal(job.title, job.description)
            else:
                proposal_text = generator.generate_proposal(job.title, job.description, budget=job.budget)
            
            proposal = Proposal(
                job_id=job_id,
                proposal_text=proposal_text,
                proposal_type=proposal_type
            )
            db.add(proposal)
            db.commit()
            
            return jsonify({
                'status': 'success',
                'proposal': {
                    'id': proposal.id,
                    'proposal_text': proposal_text,
                    'proposal_type': proposal_type
                }
            })
        finally:
            db.close()
            
    except Exception as e:
        logger.error(f"Error generating proposal: {e}")
        return jsonify({'status': 'error', 'error': str(e)}), 500

@main_bp.route('/api/proposals/<job_id>')
def get_proposals(job_id):
    db = Session()
    try:
        from app.database.models import Proposal
        proposals = db.query(Proposal).filter(Proposal.job_id == job_id).all()
        
        proposals_data = [
            {
                'id': p.id,
                'proposal_text': p.proposal_text,
                'proposal_type': p.proposal_type,
                'is_sent': bool(p.is_sent),
                'created_at': p.created_at.isoformat() if p.created_at else None
            }
            for p in proposals
        ]
        
        return jsonify({'proposals': proposals_data})
    finally:
        db.close()

@main_bp.route('/api/jobs/<job_id>')
def get_job_details(job_id):
    db = Session()
    try:
        job = crud.get_job_by_id(db, job_id)
        if not job:
            return jsonify({'status': 'error', 'message': 'Job not found'}), 404
        
        job_data = {
            'id': job.id,
            'job_id': job.job_id,
            'title': job.title,
            'description': job.description,
            'category': job.category,
            'budget': job.budget,
            'budget_type': job.budget_type,
            'complexity': job.complexity,
            'status': job.status,
            'platform': job.platform,
            'url': job.url,
            'skills_required': job.skills_required,
            'posted_date': job.posted_date.isoformat() if job.posted_date else None,
            'created_at': job.created_at.isoformat() if job.created_at else None
        }
        
        return jsonify({'job': job_data})
    finally:
        db.close()
