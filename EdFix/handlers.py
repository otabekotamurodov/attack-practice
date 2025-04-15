from aiogram import Router, types, F
from utils import download_and_merge, check_if_segment

router = Router()
user_data = {}

@router.message(F.text == "/start")
async def start_handler(message: types.Message):
    await message.answer("Salom! 3 qadam:\n1. Video link\n2. Audio link\n3. Fayl nomi")

@router.message(F.text)
async def handle_input(message: types.Message):
    user_id = message.from_user.id
    text = message.text.strip()

    if user_id not in user_data:
        user_data[user_id] = {}

    # 1. VIDEO link
    if 'video' not in user_data[user_id]:
        if await check_if_segment(text):
            await message.answer("❌ Bu video link segmentli ko‘rinmoqda. Iltimos, to‘liq faylga oid link yuboring.")
            return
        user_data[user_id]['video'] = text
        await message.answer("✅ Video link qabul qilindi. Endi audio linkni yuboring.")

    # 2. AUDIO link
    elif 'audio' not in user_data[user_id]:
        if await check_if_segment(text):
            await message.answer("❌ Audio link segmentli. Iltimos, to‘liq audio faylga oid link yuboring.")
            return
        user_data[user_id]['audio'] = text
        await message.answer("✅ Audio link qabul qilindi. Endi yakuniy fayl nomini yuboring.")

    # 3. FAYL NOMI
    else:
        filename = text if text.endswith('.mp4') else text + '.mp4'
        status_msg = await message.answer("⏳ Yuklanmoqda va birlashtirilmoqda...")

        async def progress_callback(msg_text):
            await status_msg.edit_text(msg_text)

        result = await download_and_merge(
            user_data[user_id]['video'],
            user_data[user_id]['audio'],
            filename,
            progress_callback=progress_callback
        )

        if result:
            await status_msg.edit_text(f"✅ Tayyor. Fayl saqlandi.")
        else:
            await status_msg.edit_text("❌ Xatolik yuz berdi.")
        user_data.pop(user_id)
