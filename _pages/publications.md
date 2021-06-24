---
layout: archive
title: "Publications"
permalink: /publications/
author_profile: true
---

{% if author.googlescholar %}
  You can also find my articles on <u><a href="{{author.googlescholar}}">my Google Scholar profile</a>.</u>
{% endif %}

{% include base_path %}



{% for post in site.publications reversed %}
  {{post.title}}
  {{post.date | date: "%Y"}}
  [Details]({{ base_path }}{{post.permalink}})
  [Download]({{post.paperurl}})
{% endfor %}
