const OpenAI = require("openai");

const express = require("express");
const bodyParser = require("body-parser");

const app = express();
const port = process.env.PORT || 3000;

// Replace with your OpenAI API key
const apiKey = "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";

const openai = new OpenAI({
  apiKey: apiKey,
});

app.use(bodyParser.json());

app.post("/complete", async (req, res) => {
  try {
    const { content } = req.body;

    const completion = await openai.chat.completions.create({
      messages: [
        {
          role: "system",
          content:
            "Sửa lỗi chính tả câu sau nhưng không thêm các dấu chấm phẩy, không tự động viết hoa: " +
            content,
        },
      ],
      model: "gpt-3.5-turbo",
    });

    res.json({ response: completion.choices[0].message.content });
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: "Internal Server Error" });
  }
});

app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
