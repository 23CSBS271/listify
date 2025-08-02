from core.models import ReminderLog, Task  # import your model
from django.utils import timezone

def send_task_reminder_email(user_email, user_name, task_title, task_deadline, reminder_type='deadline', task=None):
    subject = f"⏰ Task Deadline Reminder: {task_title}"
    deadline_str = task_deadline.strftime('%B %d, %Y at %I:%M %p')

    html_content = f"""
    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto;">
        <h2>Task Reminder</h2>
        <p>Hi {user_name},</p>
        <p>This is a reminder that the task <strong>{task_title}</strong> is due on <strong>{deadline_str}</strong>.</p>
        <p>Please take necessary action.</p>
        <br>
        <p>— Task Manager</p>
    </div>
    """

    try:
        #email = EmailMessage(subject, html_content, settings.DEFAULT_FROM_EMAIL, [user_email])
        #email.content_subtype = 'html'
        #email.send()

        if task:
            ReminderLog.objects.create(
                task=task,
                sent_at=timezone.now(),
                reminder_type=reminder_type,
                status='sent',
                message=f"Reminder email sent for task: {task.title}"
            )

        return True

    except Exception as e:
        print(f"Failed to send email: {e}")
        if task:
            ReminderLog.objects.create(
                task=task,
                sent_at=timezone.now(),
                reminder_type=reminder_type,
                status='failed',
                message=str(e)
            )
        return False
