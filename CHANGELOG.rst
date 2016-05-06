CHANGELOG
=========

Revision 6e97fbd (06.05.2016, 15:23 UTC)
----------------------------------------

* LUN-2958

  * Drop *plugin* from cms-plugin name.
  * Add messages.

* LUN-2965

  * Remove style fix. The fix should be general for all checbox inputs.
  * Remove workarounds. Make PosterImage and ButtonWidget extend Widget.

* Misc commits

  * Update setup.py

Revision 6e2a504 (08.04.2016, 12:47 UTC)
----------------------------------------

* LUN-2842

  * Remove compiled css files.
  * Use setuptools-tasks for static files compiling.

* Misc commits

  * Update setup.py version to 0.7.0.pbs.14.

Revision 3529611 (11.03.2016, 13:59 UTC)
----------------------------------------

* LUN-2606

  * year placeholder could be missing if entry is older

No other commits.

Revision d3d71e6 (15.02.2016, 12:45 UTC)
----------------------------------------

* LUN-2910

  * Fix tests. Functions were turned to properties.
  * Add index to speed up selects with publication_date ordering on blog entries.
  * Cache previous/next post to remove extra costly queries.

No other commits.

Revision f15251a (04.02.2016, 15:37 UTC)
----------------------------------------

* LUN-2606

  * Fix document.write conflicts with hero snippets logic

* LUN-2786

  * Refactor sitemap to allow overriding BlogEntryPage selection.

No other commits.

Revision c562a5d (17.11.2015, 09:23 UTC)
----------------------------------------

* LUN-2739

  * entry image uploader, fix entry image progress

* LUN-2749

  * Searching for an entry with the date in the URL should be made in UTC.

* LUN-2770

  * Don't round, allow subpixel rendering
  * Add js css changes.
  * Fix tests.
  * Clean up namespace clashes.

No other commits.

Revision 387b5cb (04.11.2015, 15:07 UTC)
----------------------------------------

* LUN-2598

  * Shorter height for blog entry page short description..

* LUN-2739

  * Change variable name, add docs.
  * Change poster_image.html
  * Remove unused import.
  * Use parametric resize tests.
  * Add resize large image test.
  * More work on tests.
  * Fix image resize.

* LUN-2769

  * Move date js code back into template tag.

No other commits.

Revision 368d0c0 (28.10.2015, 12:05 UTC)
----------------------------------------

* LUN-2678

  * error borders fixed on ckeditor

* LUN-2684

  * Moved set/get outside mixin and changed private name to prevent name clashes.
  * Load cms content only when required.

* LUN-2693

  * Call abstract get_entries.
  * Extract another mixin.
  * PEP8 changes.
  * Relegete behaviour to mixin.
  * Fix tests.
  * More tests.
  * Work on tests.
  * Change date
  * Fix bad day string.
  * Add bootstrapselect widget.
  * Sort by updated date.

* Misc commits

  * Fix errors.

Revision 43b33c4 (20.10.2015, 13:23 UTC)
----------------------------------------

* LUN-2702

  * Handle new exception thrown by django.contrib.sites.models.SiteManager

* LUN-2724

  * keep the look and feel of image plugins even on blog posts

No other commits.

Revision 12da780 (13.10.2015, 13:16 UTC)
----------------------------------------

* LUN-2571

  * Fixed display for special characters.

* LUN-2664

  * Updated Credit and Caption text in blog metadata

* LUN-2675

  * fixed popup for nav tool

* LUN-2676

  * fixed proxy prefix for blogs * django 1.8 - request context needs to have a bounded template in order for context processors to be called

* Misc commits

  * Add missing migration 0003.

Revision bae19d3 (28.09.2015, 11:48 UTC)
----------------------------------------

* LUN-2591

  * added sites ordering for changelist view

* LUN-2592

  * added chosen widget for site selector

* LUN-2639

  * publish actions visible by default

* LUN-2654

  * fixed admin column header to update at

* Misc commits

  * Django 1.8: removed add/change/delete related buttons from filer widgets
  * Django 1.8 upgrade: removed some django1.9 deprecation warnings
  * Django 1.8 upgrade

Revision ada1646 (21.09.2015, 09:40 UTC)
----------------------------------------

* LUN-2638

  * entries sorting should remain by pub date

* LUN-2644

  * Firefox bug fixed with wrong size of Default image

* Misc commits

  * Add missing migrations.

Revision 8289e4b (12.09.2015, 11:25 UTC)
----------------------------------------

* LUN-2583

  * remvoved preview

* LUN-2602

  * increase blog image size to 1280 to fit 1280 template, restyle image metadata to match playlist player style

* LUN-2620

  * capitalize the Branding image label
  * capitalize Save and continue button
  * toggles with help text fixed
  * added icon to Publish/Unpublish button

* Misc commits

  * Added missing migration for description updates on models.

Revision 43a9a05 (04.09.2015, 09:06 UTC)
----------------------------------------

* LUN-2569

  * refactor after code review
  * missplaced elements on Blogs

* LUN-2576

  * next button not styled

* LUN-2588

  * Apply Ace theme to blog river plugin admin

* LUN-2596

  * refactor after fieldset elements have changed their sizes

No other commits.

Revision d72c5a3 (28.08.2015, 08:54 UTC)
----------------------------------------

* LUN-2310

  * customized the -open navigation tool- button
  * pop-up forms styled according to Ace theme
  * updated script to a later version so it fixes the $.browser issue
  * blogs updates to match the ace theme
  * title updated + reorder of pagination
  * breadcrumb updated

No other commits.

Revision 715220d (30.07.2015, 09:11 UTC)
----------------------------------------

* LUN-2307

  * fixed bug with uppercase blog info

* Misc commits

  * Shouldn't enforce plugin discovery at forms import. Plugins should get discovered when all apps are loaded.
  * Fixed settings based image storage so that django doesn't detect migration changes when storage gets changed

Revision 7bd69b1 (21.07.2015, 11:41 UTC)
----------------------------------------

No new issues.

* Misc commits

  * Fixed "You can't specify target table for update in FROM clause on mysql backend"
  * Django recommends using __unicode__: https://docs.djangoproject.com/en/1.8/ref/unicode/#choosing-between-str-and-unicode
  * fixed categories widget on blog entry form
  * Django 1.7: fixed empty slug for reverse
  * Django 1.7: fixed empty slug for reverse

Revision b7627f5 (17.07.2015, 14:40 UTC)
----------------------------------------

No new issues.

* Misc commits

  * pinned version for filer pbs fork
  * tox: Don't allow django 1.8 prereleases
  * Django 1.7 upgrade: fixed entry changed form css namespace
  * Django 1.7 upgrade: fixed tests; added migrations; fixed deprecation warnings
  * Django 1.6 upgrade; fixed boolean field default; fixed admin form max rec depth
  * Django 1.6 upgrade: fixed imports; querysests vars

Revision 677b20b (15.07.2015, 07:32 UTC)
----------------------------------------

* LUN-2423

  * Fixed preview entry body.

No other commits.

Revision 3a40c8d (03.07.2015, 14:18 UTC)
----------------------------------------

* LUN-2297

  * reafctor after switched to plain js ckeditor
  * fix CKEditor settings
  * Switch to CKEditor in blog entry

No other commits.

Revision e5ac3d4 (24.06.2015, 15:11 UTC)
----------------------------------------

No new issues.

* Misc commits

  * values() enforcing no items to be returned

Revision d299215 (16.06.2015, 13:58 UTC)
----------------------------------------

* LUN-2311

  * authors should have unique slugs

No other commits.

Revision 5e91574 (04.06.2015, 17:17 UTC)
----------------------------------------

No new issues.

* Misc commits

  * fixed tests
  * make sure first plugin is a TextPlugin
  * always use first plugin since that should be the text one
  * allow author row template to include extra data
  * allow toggler to be disabled
  * allow update_date to be set programatically * allow formsets for extended forms
  * added update date which will be used for entries ordering * update date has bigger priority than publication date
  * fixed issue with unique_together on nullable field (mysql: NULL!=NULL) * now showing "Updated at" before authors when an entry got updated after publishing
  * fixed default language for cms plugins create

Revision 7de096a (08.04.2015, 11:40 UTC)
----------------------------------------

* LUN-2141

  * Custom promo block was overrided by unuseful css from Blogger

No other commits.

Revision 6396ae4 (23.03.2015, 17:07 UTC)
----------------------------------------

* LUN-2088

  * #LUN-2088: cms_blogger font sizes and template updates

No other commits.

Revision a03520a (13.01.2015, 09:47 UTC)
----------------------------------------

* LUN-2023

  * added poster image to the OG image block; * all properties in the social links need to be urlencoded

No other commits.

Revision ab17a5f (04.11.2014, 10:08 UTC)
----------------------------------------

No new issues.

* Misc commits

  * fixed filer storage copy

Revision b56c5a0 (22.10.2014, 14:27 UTC)
----------------------------------------

* LUN-1673

  * dropping connection words from already existing categories.
  * added js validation for categories field. Also, slugs for categories will strip connection words.

* Misc commits

  * moved styles to css file.

Revision 610a704 (10.10.2014, 09:14 UTC)
----------------------------------------

* LUN-1766

  * Fix facebook sharing on mobile

* LUN-1845

  * Better namespace global styles for blog to avoid conflicts with page's style

No other commits.

Revision 4cc4f3a (15.09.2014, 08:17 UTC)
----------------------------------------

* LUN-1802

  * users should be able to add super landing pages with no title.

* LUN-1834

  * blogs with no titles should have a way to be accessed from the admin

No other commits.

Revision c4f9f88 (04.09.2014, 09:39 UTC)
----------------------------------------

* LUN-1706

  * added intermediary form for blogs with missing layouts

* Misc commits

  * "fixed tests"
  * small code changes
  * set session site for blog forms that are accesed directly from the url
  * added assertions for the intermediary blog form
  * added missing layout help text
  * added wizard forms for home blog
  * bypass page validation errors for blog add form
  * allow admin helper to be used without wizard forms
  * added missing blog layout validation for intermediate form
  * added capability to add multiple admin forms - wizard like

Revision 87990de (18.08.2014, 12:40 UTC)
----------------------------------------

* LUN-1754

  * changed except clause syntax to be forward compatible with Python 3.x
  * let django handle 404s

No other commits.

Revision 897e0b8 (05.08.2014, 12:23 UTC)
----------------------------------------

* LUN-1689

  * IE does not allow '-' character in window name

* LUN-1755

  * fixed IE javascript date parse for formatting.

* Misc commits

  * users that are not allowed on a blog's site should not have access to entries even if they are listed in the allowed users section

Revision d59a7e6 (28.07.2014, 09:22 UTC)
----------------------------------------

* LUN-1737

  * prevent multiple form submissions.

* LUN-1739

  * url for blogs feed is now named + helper that returns the rss url for a blog.

* LUN-1741

  * Match only the placeholder exactly
  * Fix removing all content when the text ends with '<br>'

No other commits.

Revision e0bc55b (18.07.2014, 12:12 UTC)
----------------------------------------

* LUN-1687

  * fixed entry template so that they use their blogs settings and not the blog passed in the context; Added home blog to default /blogs/ view.
  * added help text for new forms
  * fixed home blog admin permissions
  * users should see home blogs only for sites they have permissions on.
  * layout inline is now availble for super landing page
  * moved entry-related actions from blog admin to blog entry admin.
  * - implemented * home blog admin permissions * nav tool enabled * showing home blog nav nodes * home blog add & change forms
  * added new abstract blog that will respond to /blogs/. + refactored code so that we can reuse common pieces from abstract blog.

* LUN-1730

  * fixed toLocaleString entry pub date display issue.

* LUN-1731

  * customize layout should be a button, not a link

* LUN-1735

  * Fix long error message not wrapping

* Misc commits

  * sitemap perf improvement: select-related on blog since all blog related pages use the associated blog slug in their absolute url
  * super landing page url should be displayed in sitemaps
  * fixed tests

Revision 8112de7 (15.07.2014, 12:06 UTC)
----------------------------------------

* LUN-1659

  * Make 'sample text' disappear on any editing action in text plugin
  * Make 'Sample content' text disappear when a user clicks into the blog text editor

* LUN-1724

  * feed url now works with proxied sites

No other commits.

Revision 81ff82d (08.07.2014, 10:18 UTC)
----------------------------------------

* LUN-1619

  * pub date box should not be applied on objects taht don't have publication_date
  * added year to publish date time box

* LUN-1657

  * moving admin formfields fields around

* LUN-1677

  * layout chooser should open in a popup

* LUN-1682

  * fixed tests for admin entries permissions
  * hide admin sections if user is not allowed in any blog

* LUN-1708

  * added current working site permission checks for blogs.

* LUN-1717

  * publish fields should be aware of DST.

* Misc commits

  * removed unused import
  * comment change

Revision 0e8196c (03.07.2014, 07:34 UTC)
----------------------------------------

* LUN-1668

  * Remove entry title capitalization

* LUN-1688

  * Fix short desciption not wrapping in IE11

* LUN-1692

  * Add jshint globals
  * fix sharing buttons on templates with jQuery < 1.8 (missing on/off functions)

* LUN-1704

  * RSS feed for blog + validation for entries slugs

* Misc commits

  * rss enclosures will have length 0 in order to not impact performance
  * fixed validation for disallowed entry slugs
  * rss feeds enabled for blogs.

Revision 71feeba (30.06.2014, 08:31 UTC)
----------------------------------------

* LUN-1684

  * blog pages should only respond to urls that start with /blogs
  * allow proxy prefixes in the blogs urls

No other commits.

Revision 5f21b50 (20.06.2014, 11:53 UTC)
----------------------------------------

* LUN-1671

  * , LUN-1676: fixed navigation between entries; re-fixed blog related url patterns
  * fixed urls so they only match it it starts with blogs

* LUN-1676

  * LUN-1671, LUN-1676: fixed navigation between entries; re-fixed blog related url patterns

* LUN-1678

  * Fix Save button not working after alert is displayed

* LUN-1680

  * dot from filename extension should be stripped.

* Misc commits

  * Remove len(uploaded_poster_image)==CONTENT_LENGTH.

Revision a0cd378 (18.06.2014, 15:39 UTC)
----------------------------------------

* LUN-1655

  * Move help text on the left to avoid tooltip beeing cut off when window is too small

* LUN-1665

  * Add support for timezones that are not multiple of hours
  * Fix calendar not beeing displyed in IE 10 - this occured when the user was set in Pacific Time and the offset wasn't included in   the date string (ex: Wed Jun 18 05:21:38 PDT 2014) so the regex failed - to fix this get timezone programaticaly using the Date object methods

* LUN-1667

  * should not allow titles that generate empty slug

* Misc commits

  * Minor css fix for font size
  * Fix entry text on small break points
  * Increase image max upload size to 2.5 MB

Revision 99d6541 (16.06.2014, 14:40 UTC)
----------------------------------------

* LUN-1651

  * Fix help text alignment in FF and IE
  * Fix help text icon in FF, fix entry description

* LUN-1652

  * blog menu node text should be max 15 chars

* LUN-1653

  * Fix navigation popup not closing

* LUN-1656

  * change 480 breakpoint to be inclusive

* Misc commits

  * Fix blog header height when no image is present
  * help text changes

Revision 547f41e (13.06.2014, 16:22 UTC)
----------------------------------------

* LUN-1621

  * Add link to entry image in blog landing page and river plugin

* LUN-1642

  * fixed tests since blog creation now requires a home page on the working site.
  * a default layout will get generated for a new blog.

* LUN-1643

  * current user should be added in the blog allowed users on creation.
  * added categories to list display; * in order to not affect performance too much, restricted items per page to 50

* LUN-1645

  * Fix text deisplayed under poster image

* LUN-1648

  * changed help text + added help tooltips

* LUN-1650

  * Make header image only 100

Revision e0ab12a (12.06.2014, 12:53 UTC)
----------------------------------------

* LUN-1631

  * changed fieldset text

* LUN-1635

  * should not allow empty author names.

* LUN-1636

  * Remove image Credit/Caption on blog landing page and blog promotion plugin

* LUN-1638

  * poster image should not be displayed in the entry page unless it's enabled
  * added poster image display switch.
  * Changed some poster image help text/label

* LUN-1639

  * Update entry unpublish help text

* Misc commits

  * added tests
  * Fix number of blogs and entries in changelist.
  * Remove dafult entry H1 margin for pages that do not use bootstrap css
  * remove useless space
  * Fix title and category related messages.

Revision 8504886 (10.06.2014, 15:44 UTC)
----------------------------------------

* LUN-1626

  * Fix blog entry admin buttons after 'Reset' is pressed in FF

* LUN-1630

  * code style changes
  * if cdn domain is provided, use it as a custom domain and serve files from it.

* Misc commits

  * Drop entry pagination 'newer'/'older' text on small breakpoints
  * Prevent some style to be overridden by station styles
  * Fix menu going under blog banner

Revision 4092525 (06.06.2014, 09:05 UTC)
----------------------------------------

* LUN-1603

  * all poster images should have a fixed width/height. Smaller images will get a transparent background.

* LUN-1618

  * ignore empty values for date time widget

* Misc commits

  * improve query for getting categories names and ids
  * don't allow regular users to move entries; +tests
  * test move nothing; pep8 forms.py
  * don't test entries.exists(), entries could be []
  * river should diplay its title in the placeholder admin
  * refactoring tests; +pep8
  * changed docstring
  * don't use post_data; don't use redundant list()
  * rename blogentries to entries
  * don't use post_data; add tests for redundant moves
  * comment change.
  * test with saved entries, and one draft entry
  * increment duplicate slug when moving entry; +tests
  * minor stuff
  * move blog entries to a blog

Revision cfd3bf4 (05.06.2014, 11:59 UTC)
----------------------------------------

* LUN-1611

  * fix blog entries pagination display issues

* LUN-1612

  * , LUN-1613, LUN-1614: fix display issues on blog entry

* LUN-1613

  * LUN-1612, LUN-1613, LUN-1614: fix display issues on blog entry

* LUN-1614

  * LUN-1612, LUN-1613, LUN-1614: fix display issues on blog entry

* LUN-1620

  * Show title instead of description, remove date in entry footer

No other commits.

Revision 88c7b30 (03.06.2014, 10:37 UTC)
----------------------------------------

* LUN-1592

  * changed widget for categories in blgo river plugin.

* LUN-1594

  * fixed getting last position in the root nodes.

* LUN-1595

  * added momentjs to blog entry admin in order for the date string to be parsed correctly.

* LUN-1598

  * Fix prev/next not displayed side by side in FF

* LUN-1599

  * URL encode params for social plugins

* LUN-1601

  * Fix entry author field not expanding for long author list

* LUN-1604

  * Use escape() instead of escapejs() to HTML escape menu preview HMTL

No other commits.

Revision fe37dbb (02.06.2014, 12:24 UTC)
----------------------------------------

* LUN-1588

  * Fix blog river entry template

* LUN-1589

  * comment out search box
  * Remove search box from blog

* LUN-1590

  * Added site domain in the view on site url.

* LUN-1593

  * Improve blog river loading experince, fix 'Read more' button
  * move blog targeting js to css block

* LUN-1595

  * toLocaleString does not seem to work on all browsers. Fixed by using toString.

* Misc commits

  * Make sure blog css is not overidden by station custom css

Revision d23fb64 (30.05.2014, 08:52 UTC)
----------------------------------------

Changelog history starts here.
