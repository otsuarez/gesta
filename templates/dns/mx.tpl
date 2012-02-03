{% comment %} 
name           ttl  class   rr  pref name
example.com.        IN      MX  10   mail.example.com.
{% endcomment %}
{% if record_list %}
  {% for record in record_list %}
{% ifequal record.name "." %}
	{{record.ttl.ttl}}	IN	MX	{{record.preference}}	{{record.value}}
{% else %}
{{record.name}}	{{record.ttl.ttl}}	IN	MX	{{record.preference}}	{{record.value}}
{% endifequal %}
  {% endfor %}
{% endif %}
