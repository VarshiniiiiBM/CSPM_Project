/* USER CODE BEGIN Header */
/**
  ******************************************************************************
  * @file    usart.c
  * @brief   This file provides code for the configuration
  *          of the USART instances.
  ******************************************************************************
  * @attention
  *
  * Copyright (c) 2025 STMicroelectronics.
  * All rights reserved.
  *
  * This software is licensed under terms that can be found in the LICENSE file
  * in the root directory of this software component.
  * If no LICENSE file comes with this software, it is provided AS-IS.
  *
  ******************************************************************************
  */
/* USER CODE END Header */
/* Includes ------------------------------------------------------------------*/
#include "usart.h"

/* USER CODE BEGIN 0 */
#define number_data_pts 100


char buffer[100]={0};
struct data_struct {
	uint32_t data1;		//find trade off between printing floats vs uint32_t
	uint32_t data2;
	int data3;
};

// Two buffers instead of circular buffer architecture.
struct data_struct data_buffone[number_data_pts] = {0};
struct data_struct data_bufftwo[number_data_pts] = {0};
//struct data_struct read_buff[buffer_size] = {0};
volatile uint32_t readp = 0;
volatile uint32_t writep = 0;
bool is_buffone_full = false;
bool is_bufftwo_full = false;
/* USER CODE END 0 */

UART_HandleTypeDef huart2;

/* USART2 init function */

void MX_USART2_UART_Init(void)
{

  /* USER CODE BEGIN USART2_Init 0 */

  /* USER CODE END USART2_Init 0 */

  /* USER CODE BEGIN USART2_Init 1 */

  /* USER CODE END USART2_Init 1 */
  huart2.Instance = USART2;
  huart2.Init.BaudRate = 115200;
  huart2.Init.WordLength = UART_WORDLENGTH_8B;
  huart2.Init.StopBits = UART_STOPBITS_1;
  huart2.Init.Parity = UART_PARITY_NONE;
  huart2.Init.Mode = UART_MODE_TX_RX;
  huart2.Init.HwFlowCtl = UART_HWCONTROL_NONE;
  huart2.Init.OverSampling = UART_OVERSAMPLING_16;
  huart2.Init.OneBitSampling = UART_ONE_BIT_SAMPLE_DISABLE;
  huart2.AdvancedInit.AdvFeatureInit = UART_ADVFEATURE_NO_INIT;
  if (HAL_UART_Init(&huart2) != HAL_OK)
  {
    Error_Handler();
  }
  /* USER CODE BEGIN USART2_Init 2 */

  /* USER CODE END USART2_Init 2 */

}

void HAL_UART_MspInit(UART_HandleTypeDef* uartHandle)
{

  GPIO_InitTypeDef GPIO_InitStruct = {0};
  RCC_PeriphCLKInitTypeDef PeriphClkInit = {0};
  if(uartHandle->Instance==USART2)
  {
  /* USER CODE BEGIN USART2_MspInit 0 */

  /* USER CODE END USART2_MspInit 0 */

  /** Initializes the peripherals clock
  */
    PeriphClkInit.PeriphClockSelection = RCC_PERIPHCLK_USART2;
    PeriphClkInit.Usart2ClockSelection = RCC_USART2CLKSOURCE_PCLK1;
    if (HAL_RCCEx_PeriphCLKConfig(&PeriphClkInit) != HAL_OK)
    {
      Error_Handler();
    }

    /* USART2 clock enable */
    __HAL_RCC_USART2_CLK_ENABLE();

    __HAL_RCC_GPIOA_CLK_ENABLE();
    /**USART2 GPIO Configuration
    PA2     ------> USART2_TX
    PA3     ------> USART2_RX
    */
    GPIO_InitStruct.Pin = USART_TX_Pin|USART_RX_Pin;
    GPIO_InitStruct.Mode = GPIO_MODE_AF_PP;
    GPIO_InitStruct.Pull = GPIO_NOPULL;
    GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_VERY_HIGH;
    GPIO_InitStruct.Alternate = GPIO_AF7_USART2;
    HAL_GPIO_Init(GPIOA, &GPIO_InitStruct);

  /* USER CODE BEGIN USART2_MspInit 1 */

  /* USER CODE END USART2_MspInit 1 */
  }
}

void HAL_UART_MspDeInit(UART_HandleTypeDef* uartHandle)
{

  if(uartHandle->Instance==USART2)
  {
  /* USER CODE BEGIN USART2_MspDeInit 0 */

  /* USER CODE END USART2_MspDeInit 0 */
    /* Peripheral clock disable */
    __HAL_RCC_USART2_CLK_DISABLE();

    /**USART2 GPIO Configuration
    PA2     ------> USART2_TX
    PA3     ------> USART2_RX
    */
    HAL_GPIO_DeInit(GPIOA, USART_TX_Pin|USART_RX_Pin);

  /* USER CODE BEGIN USART2_MspDeInit 1 */

  /* USER CODE END USART2_MspDeInit 1 */
  }
}

/* USER CODE BEGIN 1 */
uint16_t GSMSendChar (uint8_t chr,uint32_t Timeout)
{
	uint32_t tickstart = HAL_GetTick();
//	if (UART_WaitOnFlagUntilTimeout(&huart2, UART_FLAG_TXE, RESET, tickstart, Timeout) != HAL_OK)
//	{
//		return 1;
//		//Error_Handler();
//	}
	while ((__HAL_UART_GET_FLAG(&huart2, UART_FLAG_TXE) ? SET : RESET) == RESET)
	{
		if (((HAL_GetTick() - tickstart) > Timeout) || (Timeout == 0U))
		{
			return 1;
		}
	}
	huart2.Instance->TDR = (uint8_t)(chr & 0xFFU);
	return 0;
}

void Usart_Transmit_Str(uint8_t *msg)
{
	uint16_t i = 0;
	while(msg[i] != '\0')
	{
//		USART_SendData(USARTx, msg[i]);
		if(GSMSendChar(msg[i],10)!= 1)
		{
			i++;
		}
	}
}

void put_data(uint32_t val1,uint32_t val2,int val3)
{
	//data_buff[readp].data1 = (uint32_t)val1; type casting seems to be wrong approach for float
	// Select the buffer
//	uint32_t* bs_data = &val1; // stack address mostly.
//	data_buff[readp].data1 = *bs_data;
//	data_buff[readp].data2 = (uint32_t)val2;
//	data_buff[readp].data3 = (uint32_t)val3; // negative values are fine.
//	readp++;
//	readp = readp & ~buffer_size;

	static uint32_t buff_state= 0;
	switch (buff_state)
	{
	case 0:
		// Init case
		readp = 0;
		if (!is_buffone_full)
		{
			buff_state = 1;
		}
		else if (!is_bufftwo_full)
		{
			buff_state = 2;
		}
		else
		{
			buff_state = 3;
		}
		break;
	case 1:
		// Data store buff one
		data_buffone[readp].data1 = val1;
		data_buffone[readp].data2 = val2;
		data_buffone[readp].data3 = val3; // negative values are fine.
		readp++;
		if (readp >= number_data_pts)
		{
			is_buffone_full = true;
			buff_state = 0;
		}
		break;
	case 2:
		// Data store buff two
		data_bufftwo[readp].data1 = val1;
		data_bufftwo[readp].data2 = val2;
		data_bufftwo[readp].data3 = val3; // negative values are fine.
		readp++;
		if (readp >= number_data_pts)
		{
			is_bufftwo_full = true;
			buff_state = 0;
		}
		break;
	case 3:
		// both buffers are full. Wait until empty. Dont accept data case.
		if (!is_buffone_full || !is_bufftwo_full)
		{
			buff_state = 0;
		}
		break;
	}
}

void send_data_json_array(void)
{
	/* Sending data in json array format.
	 * example: {"D1":[3123123,123124124,124124124],
	 * 			 "D2":[31,32,33],
	 * 			 "D3":[200,23141241241,200]
	 * }
	 */

	//send header first
	struct data_struct* struc_p;
	struct data_struct* struc_sv;
	//writep = 0 ;
	char local_val_buff[10];
	uint32_t buff_used = 0;

	if (is_buffone_full)
	{
		struc_sv = data_buffone;
		buff_used = 1;
	}
	else if (is_bufftwo_full)
	{
		struc_sv = data_bufftwo;
		buff_used = 2;
	}
	else
	{
		return;
	}

	snprintf(buffer,100,"{\"D1\":[");
	Usart_Transmit_Str(buffer);

	struc_p = struc_sv;
	//send data byte by byte
	for (int i=0;i<number_data_pts;i++)
	{
		// data 1 float
		snprintf(local_val_buff,10,"%u",(unsigned int)struc_p->data1);
		if (i<number_data_pts-1)
		{
			strcat(local_val_buff,",");
		}
		struc_p++;
		Usart_Transmit_Str(local_val_buff);
	}

	snprintf(buffer,100,"],\"D2\":[");
	Usart_Transmit_Str(buffer);

	struc_p = struc_sv;
	//send data byte by byte
	for (int i=0;i<number_data_pts;i++)
	{
		// data 1 float
		snprintf(local_val_buff,10,"%u",(unsigned int)struc_p->data2);
		if (i<number_data_pts-1)
		{
			strcat(local_val_buff,",");
		}
		struc_p++;
		Usart_Transmit_Str(local_val_buff);
	}
	snprintf(buffer,100,"],\"D3\":[");
	Usart_Transmit_Str(buffer);

	struc_p = struc_sv;
	//send data byte by byte
	for (int i=0;i<number_data_pts;i++)
	{
		// data 1 float
		snprintf(local_val_buff,10,"%u",(unsigned int)struc_p->data3);
		if (i<number_data_pts-1)
		{
			strcat(local_val_buff,",");
		}
		struc_p++;
		Usart_Transmit_Str(local_val_buff);
	}

	//Footer
	snprintf(buffer,100,"]}\n");
	Usart_Transmit_Str(buffer);

	if (buff_used == 1)
	{
		is_buffone_full = false;
	}
	else if(buff_used == 2 )
	{
		is_bufftwo_full = false;
	}
}
/* USER CODE END 1 */
