# YouTube Full - API Configuration

**Skill:** youtube-full  
**Provider:** TranscriptAPI.com  
**Account:** sam@cubiczan.com  
**Status:** ✅ ACTIVE

---

## API Key

**Key:** `sk_UoKXwINJ-nsnUDpa_7k4cbsGgqdGHGyc8BxJU3BR-lQ`

**Environment Variable:**
```bash
export TRANSCRIPT_API_KEY="sk_UoKXwINJ-nsnUDpa_7k4cbsGgqdGHGyc8BxJU3BR-lQ"
```

---

## Credits

**Free Tier:** 100 credits on signup  
**Cost:** 1 credit per API call

| Endpoint | Cost |
|----------|------|
| Transcript | 1 credit |
| Search | 1 credit |
| Channel/Videos | 1 credit/page |
| Channel/Resolve | FREE |
| Channel/Latest | FREE |

---

## Usage Examples

### Get Transcript
```bash
curl -s "https://transcriptapi.com/api/v2/youtube/transcript?video_url=VIDEO_URL&format=text" \
  -H "Authorization: Bearer $TRANSCRIPT_API_KEY"
```

### Search YouTube
```bash
curl -s "https://transcriptapi.com/api/v2/youtube/search?q=machine+learning&limit=10" \
  -H "Authorization: Bearer $TRANSCRIPT_API_KEY"
```

### Get Channel Videos
```bash
curl -s "https://transcriptapi.com/api/v2/youtube/channel/videos?channel=@TED" \
  -H "Authorization: Bearer $TRANSCRIPT_API_KEY"
```

---

## Saved Locations

API key automatically saved to:
- `/home/node/.openclaw/openclaw.json`
- `/home/node/.profile`
- `/home/node/.bashrc`
- `/home/node/.config/environment.d/transcript-api.conf`
- `/home/node/.transcriptapi`

---

## Full Documentation

See: `skills/youtube-full/SKILL.md`
