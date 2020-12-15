import pytest

from tgintegration import BotController, InvalidResponseError


@pytest.mark.asyncio
async def test_run_example(controller: BotController, client):
    await controller.clear_chat()

    async with controller.collect(count=1) as response:  # type: Response
        await controller.send_command("start")

    assert response.num_messages == 1

    async with controller.collect(count=1) as response:  # type: Response
        await client.send_message(controller.peer_id, "1")

    assert response.num_messages == 1

    inline_keyboard = response.reply_keyboard

    async with controller.collect(count=1) as response:  # type: Response
        await inline_keyboard.click(pattern="1")

    assert response.num_messages == 1

    async with controller.collect(count=2) as response:  # type: Response
        await client.send_message(controller.peer_id, "Wrong message")

    assert response.num_messages == 2
    assert "Введите число с клавиатуры" in response.full_text

    while r"Ваш результат" not in response.full_text:
        async with controller.collect(count=1) as response:  # type: Response
            await inline_keyboard.click(pattern="1")

    async with controller.collect(count=1) as response:  # type: Response
        await inline_keyboard.click(pattern="1")

    assert "Вы также можете создать свой собственный тест по команде /create" \
           in response.full_text
