{% comment %} 
name  ttl  class   rr     canonical name 
www        IN      CNAME  joe.example.com. 
{% endcomment %}
{% if record_list %}
  {% for record in record_list %}
{{record.name}}	{{record.ttl.ttl}} 	IN	CNAME	{{record.value}}.
  {% endfor %}
{% endif %}
