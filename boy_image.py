from PIL import Image, ImageDraw

def create_boy_image():
    # Create a blank image with a white background
    width, height = 400, 600
    image = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(image)

    # Draw the head (big circle)
    head_radius = 80
    head_center = (width // 2, 100)
    draw.ellipse(
        [
            (head_center[0] - head_radius, head_center[1] - head_radius),
            (head_center[0] + head_radius, head_center[1] + head_radius)
        ],
        fill='peachpuff', outline='black'
    )

    # Draw the ears (two small circles on either side of the head)
    ear_radius = 15
    left_ear_center = (head_center[0] - head_radius, head_center[1] - 10)
    right_ear_center = (head_center[0] + head_radius, head_center[1] - 10)
    draw.ellipse(
        [
            (left_ear_center[0] - ear_radius, left_ear_center[1] - ear_radius),
            (left_ear_center[0] + ear_radius, left_ear_center[1] + ear_radius)
        ],
        fill='peachpuff', outline='black'
    )
    draw.ellipse(
        [
            (right_ear_center[0] - ear_radius, right_ear_center[1] - ear_radius),
            (right_ear_center[0] + ear_radius, right_ear_center[1] + ear_radius)
        ],
        fill='peachpuff', outline='black'
    )

    # Draw the eyes (two small circles)
    eye_radius = 10
    left_eye_center = (head_center[0] - 30, head_center[1] - 20)
    right_eye_center = (head_center[0] + 30, head_center[1] - 20)
    draw.ellipse(
        [
            (left_eye_center[0] - eye_radius, left_eye_center[1] - eye_radius),
            (left_eye_center[0] + eye_radius, left_eye_center[1] + eye_radius)
        ],
        fill='black'
    )
    draw.ellipse(
        [
            (right_eye_center[0] - eye_radius, right_eye_center[1] - eye_radius),
            (right_eye_center[0] + eye_radius, right_eye_center[1] + eye_radius)
        ],
        fill='black'
    )

    # Draw the nose (a small triangle)
    nose_top = (head_center[0], head_center[1] + 10)  # Tip of the nose
    nose_left = (head_center[0] - 10, head_center[1] + 20)  # Left base of the nose
    nose_right = (head_center[0] + 10, head_center[1] + 20)  # Right base of the nose
    draw.polygon([nose_top, nose_left, nose_right], fill='black')

    # Draw the mouth (a small arc)
    mouth_start = (head_center[0] - 30, head_center[1] + 20)
    mouth_end = (head_center[0] + 30, head_center[1] + 40)
    draw.arc([mouth_start, mouth_end], start=0, end=180, fill='black', width=2)

    # Draw the neck (rectangle between head and upper body)
    upper_body_width = 100  # Width of the upper body
    upper_body_height = 100  # Height of the upper body
    neck_width = upper_body_width // 3  # 1/3 of upper body width
    neck_height = upper_body_height // 3  # 1/3 of upper body height
    neck_top = (head_center[0] - neck_width // 2, head_center[1] + head_radius)
    neck_bottom = (head_center[0] + neck_width // 2, head_center[1] + head_radius + neck_height)
    draw.rectangle(
        [neck_top, neck_bottom],
        fill='peachpuff', outline='black'
    )

    # Draw the upper body (rectangle with a yellow shirt)
    upper_body_top = (head_center[0] - upper_body_width // 2, neck_bottom[1])
    upper_body_bottom = (head_center[0] + upper_body_width // 2, neck_bottom[1] + upper_body_height)
    draw.rectangle(
        [upper_body_top, upper_body_bottom],
        fill='yellow', outline='black'
    )

    # Draw the arms with elbows
    arm_length = 80
    elbow_radius = 6

    # Left arm
    left_arm_start = (upper_body_top[0], upper_body_top[1] + 50)
    left_elbow = (left_arm_start[0] - arm_length // 2, left_arm_start[1] + 30)
    left_arm_end = (left_elbow[0] - arm_length // 2, left_elbow[1] + 30)
    draw.line([left_arm_start, left_elbow], fill='black', width=5)
    draw.line([left_elbow, left_arm_end], fill='black', width=5)
    draw.ellipse(
        [
            (left_elbow[0] - elbow_radius, left_elbow[1] - elbow_radius),
            (left_elbow[0] + elbow_radius, left_elbow[1] + elbow_radius)
        ],
        fill='peachpuff', outline='black'
    )

    # Right arm
    right_arm_start = (upper_body_bottom[0], upper_body_top[1] + 50)
    right_elbow = (right_arm_start[0] + arm_length // 2, right_arm_start[1] + 30)
    right_arm_end = (right_elbow[0] + arm_length // 2, right_elbow[1] + 30)
    draw.line([right_arm_start, right_elbow], fill='black', width=5)
    draw.line([right_elbow, right_arm_end], fill='black', width=5)
    draw.ellipse(
        [
            (right_elbow[0] - elbow_radius, right_elbow[1] - elbow_radius),
            (right_elbow[0] + elbow_radius, right_elbow[1] + elbow_radius)
        ],
        fill='peachpuff', outline='black'
    )

    # Draw the hands (small circles)
    hand_radius = 24  # Increased by a factor of 3 (original: 8)
    draw.ellipse(
        [
            (left_arm_end[0] - hand_radius, left_arm_end[1] - hand_radius),
            (left_arm_end[0] + hand_radius, left_arm_end[1] + hand_radius)
        ],
        fill='peachpuff', outline='black'
    )
    draw.ellipse(
        [
            (right_arm_end[0] - hand_radius, right_arm_end[1] - hand_radius),
            (right_arm_end[0] + hand_radius, right_arm_end[1] + hand_radius)
        ],
        fill='peachpuff', outline='black'
    )

    # Draw the lower body (rectangle with white pants)
    lower_body_top = (upper_body_top[0], upper_body_bottom[1])
    lower_body_bottom = (upper_body_bottom[0], upper_body_bottom[1] + 120)
    draw.rectangle(
        [lower_body_top, lower_body_bottom],
        fill='white', outline='black'
    )

    # Draw the legs with knees
    leg_length = 120
    knee_radius = 6

    # Left leg
    left_leg_start = (lower_body_top[0] + 20, lower_body_bottom[1])
    left_knee = (left_leg_start[0], left_leg_start[1] + leg_length // 2)
    left_leg_end = (left_knee[0], left_knee[1] + leg_length // 2)
    draw.line([left_leg_start, left_knee], fill='black', width=5)
    draw.line([left_knee, left_leg_end], fill='black', width=5)
    draw.ellipse(
        [
            (left_knee[0] - knee_radius, left_knee[1] - knee_radius),
            (left_knee[0] + knee_radius, left_knee[1] + knee_radius)
        ],
        fill='peachpuff', outline='black'
    )

    # Right leg
    right_leg_start = (lower_body_bottom[0] - 20, lower_body_bottom[1])
    right_knee = (right_leg_start[0], right_leg_start[1] + leg_length // 2)
    right_leg_end = (right_knee[0], right_knee[1] + leg_length // 2)
    draw.line([right_leg_start, right_knee], fill='black', width=5)
    draw.line([right_knee, right_leg_end], fill='black', width=5)
    draw.ellipse(
        [
            (right_knee[0] - knee_radius, right_knee[1] - knee_radius),
            (right_knee[0] + knee_radius, right_knee[1] + knee_radius)
        ],
        fill='peachpuff', outline='black'
    )

    # Draw the feet (small rectangles)
    foot_width = 30
    foot_height = 10
    draw.rectangle(
        [
            (left_leg_end[0] - foot_width // 2, left_leg_end[1]),
            (left_leg_end[0] + foot_width // 2, left_leg_end[1] + foot_height)
        ],
        fill='black'
    )
    draw.rectangle(
        [
            (right_leg_end[0] - foot_width // 2, right_leg_end[1]),
            (right_leg_end[0] + foot_width // 2, right_leg_end[1] + foot_height)
        ],
        fill='black'
    )

    # Resize the image to 1/10 of its original size
    new_width = width #// 10
    new_height = height #// 10
    resized_image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)

    return resized_image
