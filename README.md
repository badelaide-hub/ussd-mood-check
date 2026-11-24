# USSD Mood Check

Simple two-screen USSD app built with Flask for Nalo Solutions.

- **USSD Code:** *920*2024#
- **Endpoint:** https://your-app-name.onrender.com/ussd

### USSD Session Notes
- Max characters per screen: 160–182 characters (Nalo recommends keeping `MSG` under 120–160 characters)
- Session timeout: ~30s per screen (2–3 mins total)
- Response time target: < 5 seconds