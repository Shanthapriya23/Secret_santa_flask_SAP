from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, User, Wishlist, GiftLock, Task
from routes.forms import ProfileForm, WishlistForm

profile_bp = Blueprint("profile_bp", __name__)

@profile_bp.route("/", methods=["GET", "POST"])
@login_required
def profile():
    profile_form = ProfileForm()
    wishlist_form = WishlistForm()
    wishlist_gift = Wishlist.query.filter_by(user_id=current_user.id).first()
    gift_lock = GiftLock.query.filter_by(santa_id=current_user.id).first()
   
    secret_child_name = None
    task_given_to_child = None  
    secret_santa = None
    task_received_from_santa = None  

    if gift_lock:
        # Find Secret Child
        secret_child = User.query.get(gift_lock.child_id)
        secret_child_name = secret_child.name if secret_child else None

        # Check if a task was given
        task_given_to_child = Task.query.filter_by(santa_id=current_user.id, child_id=gift_lock.child_id).first()

    # Check if the user is a Secret Child (if they have a Secret Santa)
    received_gift = GiftLock.query.filter_by(child_id=current_user.id).first()
    if received_gift and received_gift.revealed:
        secret_santa = User.query.get(received_gift.santa_id)  # Fetch Secret Santa object
        task_received_from_santa = Task.query.filter_by(santa_id=received_gift.santa_id, child_id=current_user.id).first()

    if request.method == "GET":
        profile_form.address.data = current_user.address
        profile_form.contact.data = current_user.contact

    if request.method == "POST":
        print("Form Data:", request.form)
        print("Profile Form Valid:", profile_form.validate_on_submit())
        print("Current User:", current_user)
        print("Current user name:", current_user.name)
        if request.form.get("submit") == "Update Profile":
            if profile_form.validate_on_submit():
                current_user.address = profile_form.address.data
                current_user.contact = profile_form.contact.data
                print("Updating Address:", current_user.address)  
                print("Updating Contact:", current_user.contact)
                db.session.add(current_user)
                try:
                    db.session.commit()  # Commit changes
                    print("🔥 COMMIT SUCCESS")
                    flash("Profile updated successfully!", "success")
                except Exception as e:
                    db.session.rollback()
                    print("❌ DB Commit Failed:", str(e))
                    flash("Database error. Try again!", "danger")
                return redirect(url_for("profile_bp.profile"))          
            
            else:
                print("Profile Form Errors:", profile_form.errors)
                flash("Error updating profile. Please check the form.", "danger")

    return render_template("profile.html", 
    user=current_user, 
    profile_form=profile_form, 
    wishlist_form=wishlist_form, 
    wishlist_gift=wishlist_gift, 
    secret_child_name=secret_child_name, 
    task_given_to_child=task_given_to_child, 
    gift_lock=gift_lock, 
    secret_santa=secret_santa,
    task_received_from_santa=task_received_from_santa)


@profile_bp.route("/wishlist", methods=["GET", "POST"])
@login_required
def gift_asked_page():
    wishlist_form = WishlistForm()

    if request.method == "POST" and request.form.get("submit") == "Add to Wishlist":
        print("🌟 Received Wishlist Form Submission")
        print("🔍 Form Data:", request.form.to_dict())
        
        print("✅ Wishlist Form Valid?", wishlist_form.validate_on_submit())

        if wishlist_form.validate_on_submit():
            wishlist_item = Wishlist(
                user_id=current_user.id,
                gift_name=wishlist_form.gift_name.data,
                brand=wishlist_form.brand.data,
                model_version=wishlist_form.model_version.data,
                price=wishlist_form.price.data,
                amazon_link=wishlist_form.amazon_link.data,
            )

            db.session.add(wishlist_item)
            db.session.commit()

            print("🎉 Wishlist Item Saved:", wishlist_item)

            flash("Wishlist updated successfully!", "success")
            return redirect(url_for("profile_bp.gift_asked_page"))
        else:
            print("❌ Form Errors:", wishlist_form.errors)
            flash("Error adding gift to wishlist. Please check the form.", "danger")

    wishlist_items = Wishlist.query.filter_by(user_id=current_user.id).all()
    print("📜 Wishlist Items for User:", wishlist_items)

    return render_template("gift_asked_page.html", wishlist_items=wishlist_items, wishlist_form=wishlist_form)

@profile_bp.route('/profile/add_wishlist', methods=['POST'])
@login_required
def add_wishlist():
    wishlist_gift = Wishlist.query.filter_by(user_id=current_user.id).first()
    
    if wishlist_gift:
        flash("You have already added a gift to your wishlist!", "danger")
        return redirect(url_for('profile'))

    new_gift = Wishlist(user_id=current_user.id, gift_name=request.form.get("gift_name"))
    db.session.add(new_gift)
    db.session.commit()
    flash("Gift added to wishlist successfully!", "success")

    return redirect(url_for('profile'))

@profile_bp.route("/send_task_to_secret_child", methods=["GET", "POST"])
@login_required
def send_task_to_secret_child():
    gift_lock = GiftLock.query.filter_by(santa_id=current_user.id).first()
    
    if not gift_lock:
        flash("You need to lock a gift before sending tasks!", "danger")
        return redirect(url_for("profile_bp.profile"))

    secret_child = User.query.get(gift_lock.child_id)
    if not secret_child:
        flash("No Secret Child assigned.", "danger")
        return redirect(url_for("profile_bp.profile"))

    if request.method == "POST":
        task = request.form.get("task")
        if task:
            new_task = Task(santa_id=current_user.id, child_id=gift_lock.child_id, task=task)
            db.session.add(new_task)
            db.session.commit()
            flash("Task sent to your Secret Child!", "success")
            return redirect(url_for("profile_bp.profile"))
        else:
            flash("Please provide a task.", "danger")

    return render_template("tasks.html", secret_child=secret_child)


@profile_bp.route("/reveal_secret_santa", methods=["POST"])
@login_required
def reveal_secret_santa():
    gift_lock = GiftLock.query.filter_by(santa_id=current_user.id).first()
    
    if gift_lock and not gift_lock.revealed:
        gift_lock.revealed = True
        db.session.commit()
        flash("Your name has been revealed to your Secret Child!", "success")
    elif gift_lock and gift_lock.revealed:
        flash("Your name is already revealed!", "info")
    else:
        flash("You are not assigned a Secret Child yet.", "danger")

    return redirect(url_for("profile_bp.profile"))
