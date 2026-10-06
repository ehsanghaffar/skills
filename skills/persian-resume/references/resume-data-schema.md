# Resume Data Schema

JSON input structure for `generate_resume.py`.

## Top-level object

```json
{
  "candidate": { ... },
  "sections": [ ... ],
  "options": { ... }
}
```

## candidate

```json
{
  "name": "علی احمدی",
  "title": "توسعه‌دهنده Full-Stack",
  "email": "ali@example.com",
  "phone": "+98 912 123 4567",
  "location": "تهران، ایران",
  "website": "https://aliahmadi.com",
  "github": "github.com/ehsanghaffarii",
  "linkedin": "linkedin.com/in/ali-ahmadi",
  "portfolio": "https://aliahmadi.com",
  "summary": "توسعه‌دهنده با ۵ سال تجربه..."
}
```

All contact fields are optional. URLs/emails stay LTR in output.

## sections[]

Each section has a `type` and `data`.

### experience

```json
{
  "type": "experience",
  "title": "سوابق کاری",
  "items": [
    {
      "company": "Snapp",
      "role": "توسعه‌دهنده ارشد Backend",
      "type": "پرموقعیت",
      "location": "تهران",
      "start": "۱۴۰۱/۰۳",
      "end": "اکنون",
      "current": true,
      "bullets": [
        {
          "responsibility": "راه‌اندازی سرویس پرداخت",
          "action": "طراحی معماری میکروسرویس",
          "outcome": "کاهش زمان پاسخ ۸۰۰ms به ۱۲۰ms",
          "metric": "۸۵٪"
        }
      ],
      "technologies": ["Python", "Django", "FastAPI", "PostgreSQL", "Docker"]
    }
  ]
}
```

### project

Same structure as experience; adds `url` and `repo` fields.

### education

```json
{
  "type": "education",
  "title": "تحصیلات",
  "items": [
    {
      "institution": "دانشگاه تهران",
      "degree": "کارشناسی صنایع برق",
      "start": "۱۳۹۵",
      "end": "۱۳۹۹",
      "gpa": "۱۸.۵۴"
    }
  ]
}
```

### skills

```json
{
  "type": "skills",
  "title": "مهارت‌ها",
  "categories": [
    { "name": "برنامه‌نویسی", "items": ["Python", "TypeScript", "JavaScript"] },
    { "name": "فریمورک‌ها", "items": ["React", "Next.js", "Django", "FastAPI"] },
    { "name": "زیرساخت", "items": ["Docker", "Kubernetes", "AWS", "CI/CD"] }
  ]
}
```

### certification, language, award, publication

Same pattern; `items` is a flat string list or objects with `name`/`issuer`/`date`.

## options

```json
{
  "layout": "single-column" | "two-column" | "compact",
  "calendar": "persian" | "gregorian",
  "format": "pdf" | "docx",
  "targetRole": "توسعه‌دهنده Backend",
  "pageSize": "A4" | "Letter",
  "font": "Vazir" | "Sahel" | "Shabnam" | "Samim",
  "template": "classic" | "modern"
}
```

`template` selects the visual style:
- `classic` — single-column, traditional headings with underlines, sidebar contact strip
- `modern` — two-column layout, left sidebar for contact/skills, main area for experience

Defaults to `classic` when omitted.

`targetRole` is used to prioritize relevant sections; it does not
invent experience.
