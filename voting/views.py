from django.shortcuts import render, redirect
from .models import Candidate, Vote


def home(request):
    candidates = Candidate.objects.all()

    return render(request, 'voting/home.html', {
        'candidates': candidates
    })


def vote(request):
    if request.method == 'POST':

        voter_name = request.POST.get('voter_name', '').strip()
        candidate_id = request.POST.get('candidate')

        # Check if voter has already voted
        already_voted = Vote.objects.filter(
            voter_name__iexact=voter_name
        ).exists()

        if already_voted:
            return render(request, 'voting/home.html', {
                'candidates': Candidate.objects.all(),
                'error': 'This voter has already voted!'
            })

        candidate = Candidate.objects.get(id=candidate_id)

        Vote.objects.create(
            voter_name=voter_name,
            candidate=candidate
        )

        return redirect('success')

    return redirect('home')


def results(request):
    candidates = Candidate.objects.all()

    for candidate in candidates:
        candidate.vote_count = Vote.objects.filter(
            candidate=candidate
        ).count()

    winner = None

    if candidates:
        winner = max(
            candidates,
            key=lambda candidate: candidate.vote_count
        )

    return render(request, 'voting/results.html', {
        'candidates': candidates,
        'winner': winner
    })


def success(request):
    return render(request, 'voting/success.html')