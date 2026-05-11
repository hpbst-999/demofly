<div style="font-family: sans-serif; border: 1px solid #e1e4e8; border-radius: 10px; padding: 20px; background-color: #f6f8fa; color: #24292e;">
  <h2 style="border-bottom: 2px solid #0366d6; padding-bottom: 10px;">Старт проекта</h2>

  <div style="margin-bottom: 20px;">
    <h3 style="color: #0366d6;">Linux (Ubuntu)</h3>
    <code style="display: block; background: #272822; color: #f8f8f2; padding: 15px; border-radius: 5px; line-height: 1.5;">
      git clone https://github.com/hpbst-999/demofly.git && cd demofly <br>
      wget https://edu.postgrespro.ru/demo-20250901-3m.sql.gz <br>
      cp .env.example .env <br>
      docker compose up -d --build
    </code>
  </div>

  <div>
    <h3 style="color: #22863a;">Windows (PowerShell)</h3>
    <code style="display: block; background: #272822; color: #f8f8f2; padding: 15px; border-radius: 5px; line-height: 1.5;">
      git clone https://github.com/hpbst-999/demofly.git; cd demofly <br>
      iwr https://edu.postgrespro.ru/demo-20250901-3m.sql.gz -OutFile demo-20250901-3m.sql.gz <br>
      copy .env.example .env <br>
      docker-compose up -d --build
    </code>
  </div>

  <p style="margin-top: 15px; font-size: 0.9em; color: #586069;">
     <b>Прямая ссылка на базу:</b> 
    <a href="https://edu.postgrespro.ru/demo-20250901-3m.sql.gz" style="color: #0366d6; text-decoration: none;">Скачать дамп вручную</a>
  </p>
</div>
