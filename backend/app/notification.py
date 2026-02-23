import resend as resend
import os 
from dotenv import load_dotenv

load_dotenv()
resend.api_key = os.getenv("RESEND_API_KEY")

def createMessage(summary):
    week_start = summary['week_start']
    week_end = summary['week_end']
    summary_text = summary['summary_text']
    goals = "\n".join(f"- {g}" for g in summary['goals_worked_on'])
    next_steps = "\n".join(f"- {s}" for s in summary['next_steps'])
    message = f"Dates: {week_start} to {week_end}\n\n{summary_text}\n\nGoals Worked On:\n{goals}\n\nNext Steps:\n{next_steps}\n\nBest,\nReflections"
    return message
def sendEmail(summary, week_start, week_end):
    params = {
          "from": "Reflections <reflections@resend.dev>",  # use this for testing
          "to": [os.getenv("EMAIL")],
          "subject": f"Your Weekly Reflection Summary: {week_start} to {week_end}",
          "html": f"<h2>Your Weekly Reflection Summary</h2><p>{summary.replace(chr(10), '<br>')}</p>",
    }
    response = resend.Emails.send(params)
    print(f"Email sent: {response}")
