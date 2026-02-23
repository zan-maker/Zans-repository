# Yellow Pages (Zembra) API Configuration

**API Key:** `8qYVrLzjNYZVcnPSM0N3gPRddFsWXWb58k4GmTCEMQhlx0gUUhehQsPmTztblnINSC3smdyiQWeJKvASsyYNB8CT3n5eJS46Nqh90kavcdVuS2AaWBtutYyiayxdjvS7`

**Documentation:** https://docs.zembra.io/welcome-to-zembra-api-documentation

**Use:** Find local businesses by category, location, employee count

**Status:** Primary for SMB lead generation

**Configured Cron Jobs:**
- SMB Lead Generator (Wellness 125)
- Expense Reduction Lead Generator

**Example Usage:**
```bash
curl -X GET 'https://api.zembra.io/v1/businesses/search' \
-H 'Authorization: Bearer 8qYVrLzjNYZVcnPSM0N3gPRddFsWXWb58k4GmTCEMQhlx0gUUhehQsPmTztblnINSC3smdyiQWeJKvASsyYNB8CT3n5eJS46Nqh90kavcdVuS2AaWBtutYyiayxdjvS7' \
-d 'category=healthcare&location=Dallas,TX&employee_count_min=20'
```
