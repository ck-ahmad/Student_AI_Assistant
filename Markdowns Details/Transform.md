
# 🚀 Guide: Gemini **2.5 Pro**

This guide updates your project from **Gemini Pro** to **Gemini 2.5 Pro**.

---

## ✅ What Changed

### **OLD (Gemini Pro):**
```python
self.model = genai.GenerativeModel('gemini-pro')
````

### ✅ **NEW (Gemini 2.5 Pro):**

```python
self.model = genai.GenerativeModel('gemini-2.5-pro-latest')
self.generation_config = {
    'temperature': 0.7,
    'top_p': 0.95,
    'top_k': 40,
    'max_output_tokens': 4096,
}
```

---

## ✅ Why Upgrade?

| Feature          | Gemini Pro | Gemini 2.5 Pro          |
| ---------------- | ---------- | ----------------------- |
| Speed            | Good       | ✅ Faster                |
| Accuracy         | Good       | ✅ More intelligent      |
| Context Window   | 30K tokens | 🚀 **2 Million tokens** |
| Code + Reasoning | Medium     | ✅ Advanced              |
| Free to use      | Yes        | ✅ Still Free            |

---

## ✅ Files to Update

Replace model name in:

* `notes_ai.py`
* `drive_manager_ai.py`
* `health_tracker_ai.py`
* `quiz_generator_ai.py`
* `search_engine_ai.py`

---

## ✅ Auto Update Script

Create a file named **`upgrade_to_25pro.py`**:

```python
import os

files = [
    'notes_ai.py',
    'drive_manager_ai.py',
    'health_tracker_ai.py',
    'quiz_generator_ai.py',
    'search_engine_ai.py'
]

for filename in files:
    if os.path.exists(filename):
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()

        content = content.replace("'gemini-pro'", "'gemini-2.5-pro-latest'")
        content = content.replace('"gemini-pro"', '"gemini-2.5-pro-latest"')

        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)

        print(f"✅ Updated: {filename}")
    else:
        print(f"⚠️ Not found: {filename}")

print("\n🎉 All files updated to Gemini 2.5 Pro!")
```

Run:

```bash
python upgrade_to_25pro.py
```

---

## ✅ Manual Update (If Script Fails)

Search for:

```python
self.model = genai.GenerativeModel('gemini-pro')
```

Replace with:

```python
self.model = genai.GenerativeModel('gemini-2.5-pro-latest')
```

---

## ✅ Test the Model

Create **`test_25pro.py`**:

```python
import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-pro-latest")

res = model.generate_content("Say: Gemini 2.5 Pro is working!")
print(res.text)
```

Run:

```bash
python test_25pro.py
```

✅ Expected Output:

```
Gemini 2.5 Pro is working!
```

---

## ✅ Troubleshooting

| Error             | Fix                                         |
| ----------------- | ------------------------------------------- |
| `Model not found` | `pip install --upgrade google-generativeai` |
| Wrong spelling    | ✅ Must be `gemini-2.5-pro-latest`           |
| API key issue     | Make sure GEMINI_API_KEY is set             |

---

## ✅ Final Checklist

* [ ] All 5 modules updated to `gemini-2.5-pro-latest`
* [ ] `test_25pro.py` works
* [ ] No `gemini-pro` left
* [ ] Faster + smarter responses
* [ ] Ready for deployment 🚀
 
Want a stylish GitHub badge + footer section too?
```
