Telegram Channel
================

This project is part of the architecture described in:
Herrera, Andre & Yaguachi, Lady & Piedra, Nelson. (2019). Building Conversational Interface for Customer Support Applied to Open Campus an Open Online Course Provider. 11-13. 10.1109/ICALT.2019.00011.


Running scripts


``docker build -t astandre/kbsbot_oc_tc --build-arg CONNECTION_KEY=tokendeseguridad --build-arg API_KEY=616944972:AAFUU_Od5-fiEg_Oe7pV0g-aWgXuAVM0ctk . -f docker/Dockerfile``

``docker build -t astandre/kbsbot_oc_tc . -f docker/Dockerfile``


``docker run --rm  --name=oc_tc -it astandre/kbsbot_oc_tc``



