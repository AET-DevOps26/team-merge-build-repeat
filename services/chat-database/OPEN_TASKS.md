# Offene Sicherheitsaufgaben

## JWT-Authentifizierung im Chat-Service

- [ ] Den Chat-Service als OAuth2 Resource Server konfigurieren.
- [ ] `spring-security-oauth2-resource-server` und `spring-security-oauth2-jose` hinzufügen.
- [ ] Den bestehenden `BearerTokenAuthenticationFilter` durch Spring Securitys JWT-Resource-Server-Filter ersetzen.
- [ ] `issuer-uri` und `jwk-set-uri` des Identity Providers als Konfiguration hinterlegen.
- [ ] Den erlaubten JWS-Algorithmus auf den tatsächlich vom Identity Provider verwendeten asymmetrischen Algorithmus beschränken, z. B. `ES256` oder `RS256`.
- [ ] JWT-Claims mindestens für `iss`, `aud`, `exp` und `nbf` validieren.
- [ ] Im `GameAccessAuthorizer` den bereits geprüften Originaltoken aus `JwtAuthenticationToken` an die Verify-API weiterreichen.

## Game-Ownership-Verify im Application-Service

- [ ] `POST /v1/games/{gameId}/verify` implementieren.
- [ ] Den JWT dort ebenfalls vollständig prüfen und die `sub`-Claim gegen den Eigentümer des Spiels prüfen.
- [ ] Bei erlaubtem Zugriff `204 No Content`, bei ungültigem Token `401` und bei fremder oder unbekannter Game-ID `403` zurückgeben.
- [ ] Die Game-ID im Application-Service als UUID führen.

## Betrieb und Tests

- [ ] Die Verify-API nur im internen Service-Netz verfügbar machen und Bearer-Token nicht protokollieren.
- [ ] TLS für serviceübergreifende Kommunikation außerhalb eines vertrauenswürdigen lokalen Netzwerks erzwingen.
- [ ] Integrationstests mit echten, vom Test-Issuer signierten JWTs ergänzen: gültig, abgelaufen, falscher Issuer, falsche Audience, falsche Signatur und Key-Rotation.
