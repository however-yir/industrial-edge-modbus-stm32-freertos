# 工業邊緣 Modbus 通訊中介層 | Industrial Edge Modbus Middleware

本文件提供繁體中文快速導覽，完整說明請以 `README.md` 為主。

## 專案簡介

這是一個基於 STM32 + FreeRTOS 的 Modbus 通訊中介層專案，支援：

- RTU / TCP / USB-CDC
- 主站與從站
- RS232 / RS485
- 多實例並行
- USART DMA 高鮑率

## 快速開始

1. 在 STM32CubeIDE 匯入 `Examples/` 中的任一示例工程
2. 依目標硬體調整 `ModbusConfig.h`
3. 下載到開發板並啟動
4. 使用 `Script/` 內測試腳本做主從驗證

## 文件索引

- 專案主文檔：`README.md`
- 開發協議：`PROJECT_PROTOCOL.md`
- 配置模板：`config/runtime.example.env`
- 改造路線圖：`docs/modernization-roadmap.md`

## 授權

詳見 `LICENSE`。

