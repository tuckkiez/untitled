# 🚀 การตั้งค่า GitHub Pages

## ปัญหาที่พบ
```
remote: Permission to tuckkiez/untitled.git denied to github-actions[bot].
fatal: unable to access 'https://github.com/tuckkiez/untitled.git/': The requested URL returned error: 403
```

## วิธีแก้ไข

### 1. เปิดใช้งาน GitHub Pages
1. ไปที่ repository: https://github.com/tuckkiez/untitled
2. คลิก **Settings** (แท็บด้านบน)
3. เลื่อนลงไปหา **Pages** (เมนูด้านซ้าย)
4. ในส่วน **Source** เลือก **GitHub Actions**

### 2. ตั้งค่าสิทธิ์ Actions
1. ใน **Settings** ไปที่ **Actions** > **General**
2. ในส่วน **Workflow permissions** เลือก:
   - ✅ **Read and write permissions**
   - ✅ **Allow GitHub Actions to create and approve pull requests**
3. คลิก **Save**

### 3. ตรวจสอบการตั้งค่า Repository
1. ใน **Settings** > **Actions** > **General**
2. ในส่วน **Actions permissions** ตรวจสอบว่าเลือก:
   - ✅ **Allow all actions and reusable workflows**

### 4. Push การเปลี่ยนแปลง
หลังจากแก้ไข workflow แล้ว ให้ push ขึ้น GitHub:

```bash
git add .github/workflows/deploy.yml
git commit -m "🔧 Fix GitHub Pages deployment permissions"
git push origin master
```

## ✅ ผลลัพธ์ที่คาดหวัง

หลังจากตั้งค่าเสร็จ:
- 🌐 เว็บไซต์จะเข้าถึงได้ที่: https://tuckkiez.github.io/untitled/
- 🔄 จะอัพเดทอัตโนมัติทุกครั้งที่ push ไฟล์ใหม่
- 📊 แสดงผล Value Bet Analysis แบบ Interactive

## 🔧 Workflow ใหม่

ไฟล์ `.github/workflows/deploy.yml` ได้รับการอัพเดทเพื่อ:
- ✅ ใช้ permissions ที่ถูกต้อง
- ✅ ใช้ actions ล่าสุด (v4)
- ✅ แยก build และ deploy jobs
- ✅ รองรับ GitHub Pages environment

## 🚨 หากยังมีปัญหา

### ทางเลือก 1: Manual Deployment
```bash
# สร้าง gh-pages branch
git checkout --orphan gh-pages
git rm -rf .
cp index.html .
git add index.html
git commit -m "Deploy to GitHub Pages"
git push origin gh-pages
git checkout master
```

### ทางเลือก 2: ใช้ GitHub Desktop
1. เปิด GitHub Desktop
2. ไปที่ Repository Settings
3. เปิดใช้งาน GitHub Pages
4. เลือก source เป็น gh-pages branch

## 📞 ติดต่อ Support
หากยังมีปัญหา สามารถ:
1. ตรวจสอบ Actions tab ใน GitHub repository
2. ดู logs ของ workflow ที่ fail
3. ตรวจสอบ Settings > Pages ว่าตั้งค่าถูกต้อง

---

🎯 **เป้าหมาย**: ให้เว็บไซต์ Value Bet Analysis เข้าถึงได้ผ่าน GitHub Pages
