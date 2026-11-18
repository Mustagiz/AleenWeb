import re

path = 'Aleen website/index.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# 1. searchBtn.addEventListener
content = content.replace(
    "searchBtn.addEventListener('click', function () { searchOpen ? closeSearch() : openSearch(); });",
    "if (searchBtn) searchBtn.addEventListener('click', function () { searchOpen ? closeSearch() : openSearch(); });"
)

content = content.replace(
    "$('#searchClose').addEventListener('click', closeSearch);",
    "var _sc = $('#searchClose'); if (_sc) _sc.addEventListener('click', closeSearch);"
)

content = content.replace(
    "searchInput.addEventListener('input', function () { paintSearch(searchInput.value.trim()); });",
    "if (searchInput) searchInput.addEventListener('input', function () { paintSearch(searchInput.value.trim()); });"
)

content = content.replace(
    "$('#searchForm').addEventListener('submit', function (e) { e.preventDefault(); });",
    "var _sf = $('#searchForm'); if (_sf) _sf.addEventListener('submit', function (e) { e.preventDefault(); });"
)

content = re.sub(
    r"searchInput\.addEventListener\('keydown',\s*function\s*\(e\)\s*\{",
    "if (searchInput) searchInput.addEventListener('keydown', function (e) {",
    content
)

# 2. acctPop
content = content.replace(
    "$('#acctPop').addEventListener('click', function (e) {",
    "var _ap = $('#acctPop'); if (_ap) _ap.addEventListener('click', function (e) {"
)

# 3. menu
content = content.replace(
    "menuBtn.addEventListener('click', function () {",
    "if (menuBtn) menuBtn.addEventListener('click', function () {"
)

content = content.replace(
    "mnClose.addEventListener('click', closeNav);",
    "if (mnClose) mnClose.addEventListener('click', closeNav);"
)

content = content.replace(
    "mnBack.addEventListener('click', popPanel);",
    "if (mnBack) mnBack.addEventListener('click', popPanel);"
)

content = content.replace(
    "$('.mn-foot .mn-acct').addEventListener('click', closeNav);",
    "var _ma = $('.mn-foot .mn-acct'); if (_ma) _ma.addEventListener('click', closeNav);"
)

# 4. w-prev / w-next
content = content.replace(
    "$('.w-prev').addEventListener('click', function () { show(idx - 1); });",
    "var _wp = $('.w-prev'); if (_wp) _wp.addEventListener('click', function () { show(idx - 1); });"
)
content = content.replace(
    "$('.w-next').addEventListener('click', function () { show(idx + 1); });",
    "var _wn = $('.w-next'); if (_wn) _wn.addEventListener('click', function () { show(idx + 1); });"
)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)

print("Patch applied successfully")

