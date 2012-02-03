$TTL {{zone.ttl.ttl}} ; {{zone.ttl.description}} 
$ORIGIN {{zone.name}}.
@	{{zone.ttl.ttl}} 	IN	SOA	{{zone.master}}.	{{zone.soa_email}}.{{zone.master}}.	(
	{{zone.serial}}			;serial
	{{zone.soa_refresh.ttl}}	; refresh {{zone.soa_refresh.description}}
	{{zone.soa_retry.ttl}}		; retry {{zone.soa_retry.description}}
	{{zone.soa_expiry.ttl}}		; expire {{zone.soa_expiry.description}}	
	{{zone.soa_minimun.ttl}}	; minimum {{zone.soa_minimun.description}}

)
