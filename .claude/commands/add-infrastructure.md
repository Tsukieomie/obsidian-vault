---
description: Create a new technical infrastructure profile using the template
---

Create a new technical infrastructure profile in the Technical/ folder.

Follow these steps:
1. Ask the user for the infrastructure name (domain, AS number, or service name)
2. Use the Technical Infrastructure Template from Templates/Technical Infrastructure Template.md
3. Create the file in Technical/ with an appropriate filename
4. Fill in whatever technical information the user provides
5. Add the infrastructure to Entity Index.md
6. Add an entry to Timeline.md documenting the discovery
7. Update relevant analysis documents (Connection Map, Threat Assessment)

Prompt the user for:
- Domain/hostname or infrastructure name
- Type (network, domain, server, service)
- Status (active, inactive, abandoned)
- IP address(es)
- AS number (if applicable)
- Hosting provider
- Registration information
- Observed capabilities
- Connections to entities (who operates it)

After creating the profile, ask if they want to:
- Add IOCs to the document
- Set up monitoring
- Update the Connection Map with this infrastructure
