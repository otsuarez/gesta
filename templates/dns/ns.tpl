{% comment %} 
name           ttl  class   rr     name
example.com.        IN      NS      ns1.example.com.
arreglar, si es numerico no lleva el punto al final, si no, si
{% endcomment %}
{% if record_list %}
  {% for record in record_list %}
	{% ifequal record.name "." %}
{{record.ttl.ttl}} 	IN	NS	{{record.value}}
	{% else %}
{{record.name}}	{{record.ttl.ttl}} 	IN	NS	{{record.value}}
	{% endifequal %}
  {% endfor %}
{% endif %}
{% if zone %}
{{zone.ttl.ttl}} 	IN	NS	{{zone.master}}.
{% endif %}
