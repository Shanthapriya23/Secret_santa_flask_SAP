from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db  # Import db
from models import Wishlist, GiftLock, User

gifts_bp = Blueprint('gifts', __name__)

@gifts_bp.route('/view', methods=['GET'])
@login_required
def view_gift_pool():
    """Show all gifts except the ones added by the current user and gifts that are already locked."""
    
    # Get IDs of locked gifts
    locked_gift_ids = db.session.query(GiftLock.gift_id).all()
    locked_gift_ids = {gift_id[0] for gift_id in locked_gift_ids}  # Convert to set

    # Fetch gifts that are NOT added by the current user AND are NOT locked
    available_gifts = Wishlist.query.filter(
        (Wishlist.user_id != current_user.id) &  # Exclude own gifts
        (~Wishlist.id.in_(locked_gift_ids))  # Exclude locked gifts
    ).all()

    return render_template('gift_registration.html', gifts=available_gifts)

@gifts_bp.route('/lock/<int:gift_id>', methods=['POST'])
@login_required
def lock_gift(gift_id):
    """Lock a gift for the current user and assign them a Secret Child."""
    gift = Wishlist.query.get_or_404(gift_id)

    # Ensure the user is not locking their own gift
    if gift.user_id == current_user.id:
        flash("You cannot lock a gift from your own wishlist!", "danger")
        return redirect(url_for("gifts.view_gift_pool"))

    # Check if the gift is already locked
    existing_lock = GiftLock.query.filter_by(gift_id=gift_id).first()
    if existing_lock:
        flash("This gift has already been locked by another user!", "danger")
        return redirect(url_for("gifts.view_gift_pool"))

    # Find a Secret Child (gift owner)
    child_user = User.query.get(gift.user_id)

    # Lock the gift for the current user (Secret Santa)
    new_lock = GiftLock(santa_id=current_user.id, child_id=child_user.id, gift_id=gift_id)
    db.session.add(new_lock)
    db.session.commit()

    flash(f"You have locked a gift for {child_user.name}!", "success")
    return redirect(url_for("gifts.view_gift_pool"))
