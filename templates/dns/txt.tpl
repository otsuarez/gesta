{% comment %} 
name  ttl  class   rr     text
joe        IN      TXT    "Located in a black hole"
{% endcomment %}
{% if record_list %}
  {% for record in record_list %}
{% ifequal record.name "." %}
	{{record.ttl.ttl}} 	IN	TXT	"{{record.value}}"
{% else %}
{{record.name}}	{{record.ttl.ttl}} 	IN	TXT	"{{record.value}}"
{% endifequal %}
  {% endfor %}
{% endif %}
