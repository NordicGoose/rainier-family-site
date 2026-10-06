# rainier-family-site

Static public welcome, household-access directions, and legal pages for Rainier Family.
The existing `CNAME` keeps `rainier.app`; `.nojekyll` keeps these plain files suitable for
the existing GitHub Pages host. No build, dependencies, analytics, forms, or API calls.

`household.html` links to the existing private HTTPS gateway. It does not authenticate,
enroll devices, proxy household content, or change the separate public guest allowlist.
Device enrollment, passkeys, app lock, per-user permissions, and private network access
remain in Rainier. No setup codes, account details, or household data belong in this repo.
The native app has no invented download or deep link here.

Source draft only: review the complete patch, run `python3 test_site.py`, and preview
the two changed pages on desktop/mobile before publishing through the existing Pages
workflow. Verify the private link on an enrolled device separately. Publishing these
files does not qualify private app sign-in or provider/account connectivity.
The existing privacy and terms pages remain byte-identical.
