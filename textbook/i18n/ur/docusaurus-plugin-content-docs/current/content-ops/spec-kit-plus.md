---
id: spec-kit-plus
title: "مواد کنٹرول — Spec-Kit Plus ورک فلو"
sidebar_position: 20
---

ہم Spec-Kit Plus ( `.specify/` میں موجود) استعمال کرتے ہیں تاکہ نصاب ہم آہنگ اور قابلِ جائزہ رہے۔

## تحریری بہاؤ
1. **ارادہ درج کریں**: صارف کی درخواستیں Prompt History Records میں `history/prompts/` کے تحت نوٹ کریں۔  
2. **اسپیک/پلان/ٹاسکس**: `.specify/templates/` میں ٹیمپلیٹس سے فیچر یا باب کے لیے تقاضے لکھیں۔  
3. **پیشگی جانچ**:  
   ```powershell
   .specify/scripts/powershell/check-prerequisites.ps1 -Json -RequireTasks -IncludeTasks
   ```  
   یہ یقینی بناتا ہے کہ موجودہ فیچر کے لیے `spec.md`, `plan.md`, `tasks.md` موجود ہیں۔
4. **مواد لکھیں**: `textbook/docs/` میں MDX تحریر کریں، مشترکہ سیکشنز (مقاصد، کلیدی نکات، مثالیں، چیک لسٹ) فالو کریں۔  
5. **توثیق**: `npm run build` سے لنک/فارمیٹ چیک کریں؛ کوڈ قابلِ عمل رکھیں۔  
6. **نتیجہ درج کریں**: ٹاسکس/چیک لسٹس اپڈیٹ کریں، اور PHR میں خلاصہ شامل کریں۔

## اسٹائل گارڈ ریلز
- مختصر سرخیاں، سادہ زبان، اور قابلِ عمل کوڈ (Python/JS) استعمال کریں۔  
- چیک لسٹس عمل کے قابل ہوں اور آخر میں “اجتناب کی غلطیاں” شامل کریں۔  
- SVG/PNG کو ترجیح دیں؛ ڈایاگرام Mermaid یا Draw.io ایکسپورٹس سے بنائیں۔  
- سیکریٹس ہارڈ کوڈ نہ کریں؛ `.env` پیٹرن استعمال کریں۔

## کہاں کیا ہے؟
- `.specify/`: Spec-Kit Plus ٹیمپلیٹس اور اسکرپٹس۔  
- `specs/<feature>/`: ہر فیچر برانچ کے لیے اسپیک/پلان/ٹاسکس۔  
- `history/prompts/<feature>/`: Prompt History Records۔  
- `textbook/docs/`: باب کا مواد (MDX)۔
