{% comment %} 
name  ttl  class   rr     ip
joe        IN      A      192.168.254.3
{% endcomment %}
{% if record_list %}
  {% for record in record_list %}
{% ifequal record.name "." %}
	{{record.ttl.ttl}} 	IN	A	{{record.value}}
{% else %}
{{record.name}}	{{record.ttl.ttl}} 	IN	A	{{record.value}}
{% endifequal %}
  {% endfor %}
{% endif %}
