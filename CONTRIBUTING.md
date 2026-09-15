# Contributing to Sabal

Thank you for wanting to help. Sabal is a free, open study aid for the Florida
Civic Literacy Exam, and it gets better when people contribute. There is no
Discord to join and no gatekeeper to impress — everything happens here, in the
issue tracker and in pull requests, on your schedule.

## The two things this project always needs

1. **Better content.** The exam bank, the explanations, and the reading material
   are the heart of Sabal. If you spot a question with a wrong fact, a distractor
   that isn't really wrong, or a standard that's under-covered, that's the most
   valuable report you can make.
2. **Bug reports.** Something broken on the site? Open an issue with what you did,
   what you expected, and what happened. A screenshot or the browser/device helps.

## Reporting a bug

Open an issue and include:

- What you were doing
- What you expected
- What actually happened
- Browser and device, if relevant

If you'd rather not file an issue, that's fine — but an issue is how a fix actually
gets tracked and shipped.

## Contributing code

1. Fork the repository and create a branch.
2. Make your change. Keep it small and focused — one fix or feature per pull
   request is much easier to review than five.
3. Run the test suite before you open the PR:

   ```bash
   python3 -m unittest discover -s tests -t .
   ```

4. Open the pull request and describe *what* you changed and *why*.

There are no style gatekeepers, but please match the surrounding code and keep
changes readable. If a change touches behavior, add or update a test.

## Contributing content

Questions and readings are data in `data/fcle.db`. If you're adding or correcting
content, open an issue first describing the change and the source you're drawing
on — factual claims need a source. Pull requests that add content should note the
source in the PR description so it can go into `ATTRIBUTION.md`.

## Licensing your contribution

By contributing you agree to license:

- **code** under [Apache-2.0](LICENSE), and
- **content** under [CC BY-NC-SA 4.0](LICENSE-CONTENT).

That keeps Sabal free and open, now and for everyone who forks it.

## Ground rules

- Be kind. This is an educational resource for students, not a battleground.
- No unsolicited "AI can fix everything" rewrites of the Study Coach. The coach
  is deliberately deterministic — that is a design decision, not a gap. See the
  README.
- The maintainer reviews on his own schedule. A slow response isn't a rejection.

Thank you.
