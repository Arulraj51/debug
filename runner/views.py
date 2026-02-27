import subprocess
import tempfile
from django.conf import settings
from django.shortcuts import render, get_object_or_404
from .models import Challenge
from django.views.decorators.cache import never_cache


@never_cache
def challenge_view(request, id):
    challenge = get_object_or_404(Challenge, id=id)

    result_message = ""
    master_flag = None

    prev_challenge = Challenge.objects.filter(id__lt=challenge.id).order_by('-id').first()
    next_challenge = Challenge.objects.filter(id__gt=challenge.id).order_by('id').first()

    # Initialize solved list in session
    if "solved" not in request.session:
        request.session["solved"] = []

    if request.method == "POST":
        user_code = request.POST.get("code")

        with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as temp:
            temp.write(user_code.encode())
            temp.close()

        try:
            result = subprocess.run(
                ["python", temp.name],
                capture_output=True,
                text=True,
                timeout=3
            )

            output = result.stdout.strip()
            expected = challenge.expected_output.strip()

            output_lines = [line.strip() for line in output.splitlines()]
            expected_lines = [line.strip() for line in expected.splitlines()]

            if output_lines == expected_lines:
                result_message = "Correct! ✅"

                # Add challenge to solved list
                solved = request.session["solved"]
                if challenge.id not in solved:
                    solved.append(challenge.id)
                    request.session["solved"] = solved

                # Check if ALL challenges solved
                total = Challenge.objects.count()
                if len(solved) == total:
                    master_flag = settings.MASTER_FLAG

            else:
                result_message = "Wrong answer. Try again!"

        except subprocess.TimeoutExpired:
            result_message = "Time limit exceeded!"
        except Exception as e:
            result_message = f"Error: {str(e)}"

    return render(request, "runner/challenge.html", {
        "challenge": challenge,
        "result": result_message,
        "prev_challenge": prev_challenge,
        "next_challenge": next_challenge,
        "master_flag": master_flag,
    })


def index(request):
    return render(request, 'runner/index.html')