
class base_element:
    """
    Page Object Repo
    """
    pages = 5
    base_url = "https://github.com/"
    api_query = "https://github.com/search?p={}&q=security&type=Repositories"
    per_page_result = 10
    search_bar = ".form-control.input-sm.header-search-input.jump-to-field.js-jump-to-field.js-site-search-focus"
    suggestion = "#jump-to-suggestion-search-global .jump-to-suggestion-name.js-jump-to-suggestion-name.flex-auto.overflow-hidden.text-left.no-wrap.css-truncate.css-truncate-target"
    search_result = ".repo-list-item.hx_hit-repo.d-flex.flex-justify-start.py-4.public.source:nth-child({})"
    title = ":nth-child({}) > div > div > div > a.v-align-middle"
    description = ":nth-child({}) > div > p.mb-1"
    tag = "a.topic-tag.topic-tag-link.f6.px-2.mx-0"
    stars = "div > a.Link--muted"
    language = "div.mr-3 > span"
    lincencedBy = "div.d-flex.flex-wrap.text-small.color-fg-muted > div:nth-child(3)"
    updateTime = "div.d-flex.flex-wrap.text-small.color-fg-muted > div:nth-child(4)"