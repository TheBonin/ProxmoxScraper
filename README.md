# ProxmoxScraper
A performance scraper for a proxmox node

# Architecture
Documentations i came up with while developing this project

## Services
<img width="909" height="428" alt="{52F52447-87A8-4B05-A840-507E3FD2E82F}" src="https://github.com/user-attachments/assets/5a5cc3d9-a7ea-44fd-b343-9d68f5611a98" />

- **Python:**
Scraper. Get relevant info from ProxMox and insrt them on on each database based on it's needs.
- **MySQL:**
Responsable for dealing with more important and structured information as daily or monthly logs.
- **Redis:**
Responsable for recieving and delivering information quickly from the scraper, garanteeing fast responses to the API causing the web dashboard to respond faster.
- **HTML + CSS:**
Responsble fo the front-end (WIP)

## Entity-Relationship Diagram (ERD)
<img width="1132" height="607" alt="{9CE119BC-FA4D-4536-8D5D-EABE666972B5}" src="https://github.com/user-attachments/assets/27dc883a-c947-4da6-bde9-9b981cfb7ffe" />

