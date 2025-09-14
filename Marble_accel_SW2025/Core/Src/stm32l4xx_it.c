/* USER CODE BEGIN Header */
/**
  ******************************************************************************
  * @file    stm32l4xx_it.c
  * @brief   Interrupt Service Routines.
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
#include "main.h"
#include "stm32l4xx_it.h"
/* Private includes ----------------------------------------------------------*/
/* USER CODE BEGIN Includes */
#include "tim.h"
#include "usart.h"
/* USER CODE END Includes */

/* Private typedef -----------------------------------------------------------*/
/* USER CODE BEGIN TD */

/* USER CODE END TD */

/* Private define ------------------------------------------------------------*/
/* USER CODE BEGIN PD */

/* USER CODE END PD */

/* Private macro -------------------------------------------------------------*/
/* USER CODE BEGIN PM */

/* USER CODE END PM */

/* Private variables ---------------------------------------------------------*/
/* USER CODE BEGIN PV */
volatile uint32_t marble_inside_flag = 0;
volatile uint32_t marble_exit_flag = 0;
volatile uint32_t marble_count = 0;
volatile uint32_t adc1_new_val_flag = 0;
volatile uint32_t adc2_new_val_flag = 0;

uint32_t adc1_running_sum = 0;
uint32_t adc2_running_sum = 0;

uint32_t calib_count = 0;
/* USER CODE END PV */

/* Private function prototypes -----------------------------------------------*/
/* USER CODE BEGIN PFP */

/* USER CODE END PFP */

/* Private user code ---------------------------------------------------------*/
/* USER CODE BEGIN 0 */

/* USER CODE END 0 */

/* External variables --------------------------------------------------------*/
extern ADC_HandleTypeDef hadc1;
extern ADC_HandleTypeDef hadc2;
extern TIM_HandleTypeDef htim3;
extern UART_HandleTypeDef huart2;
/* USER CODE BEGIN EV */
extern uint32_t mag_hor;
extern uint32_t mag_ver;
/* USER CODE END EV */

/******************************************************************************/
/*           Cortex-M4 Processor Interruption and Exception Handlers          */
/******************************************************************************/
/**
  * @brief This function handles Non maskable interrupt.
  */
void NMI_Handler(void)
{
  /* USER CODE BEGIN NonMaskableInt_IRQn 0 */

  /* USER CODE END NonMaskableInt_IRQn 0 */
  /* USER CODE BEGIN NonMaskableInt_IRQn 1 */
   while (1)
  {
  }
  /* USER CODE END NonMaskableInt_IRQn 1 */
}

/**
  * @brief This function handles Hard fault interrupt.
  */
void HardFault_Handler(void)
{
  /* USER CODE BEGIN HardFault_IRQn 0 */

  /* USER CODE END HardFault_IRQn 0 */
  while (1)
  {
    /* USER CODE BEGIN W1_HardFault_IRQn 0 */
    /* USER CODE END W1_HardFault_IRQn 0 */
  }
}

/**
  * @brief This function handles Memory management fault.
  */
void MemManage_Handler(void)
{
  /* USER CODE BEGIN MemoryManagement_IRQn 0 */

  /* USER CODE END MemoryManagement_IRQn 0 */
  while (1)
  {
    /* USER CODE BEGIN W1_MemoryManagement_IRQn 0 */
    /* USER CODE END W1_MemoryManagement_IRQn 0 */
  }
}

/**
  * @brief This function handles Prefetch fault, memory access fault.
  */
void BusFault_Handler(void)
{
  /* USER CODE BEGIN BusFault_IRQn 0 */

  /* USER CODE END BusFault_IRQn 0 */
  while (1)
  {
    /* USER CODE BEGIN W1_BusFault_IRQn 0 */
    /* USER CODE END W1_BusFault_IRQn 0 */
  }
}

/**
  * @brief This function handles Undefined instruction or illegal state.
  */
void UsageFault_Handler(void)
{
  /* USER CODE BEGIN UsageFault_IRQn 0 */

  /* USER CODE END UsageFault_IRQn 0 */
  while (1)
  {
    /* USER CODE BEGIN W1_UsageFault_IRQn 0 */
    /* USER CODE END W1_UsageFault_IRQn 0 */
  }
}

/**
  * @brief This function handles System service call via SWI instruction.
  */
void SVC_Handler(void)
{
  /* USER CODE BEGIN SVCall_IRQn 0 */

  /* USER CODE END SVCall_IRQn 0 */
  /* USER CODE BEGIN SVCall_IRQn 1 */

  /* USER CODE END SVCall_IRQn 1 */
}

/**
  * @brief This function handles Debug monitor.
  */
void DebugMon_Handler(void)
{
  /* USER CODE BEGIN DebugMonitor_IRQn 0 */

  /* USER CODE END DebugMonitor_IRQn 0 */
  /* USER CODE BEGIN DebugMonitor_IRQn 1 */

  /* USER CODE END DebugMonitor_IRQn 1 */
}

/**
  * @brief This function handles Pendable request for system service.
  */
void PendSV_Handler(void)
{
  /* USER CODE BEGIN PendSV_IRQn 0 */

  /* USER CODE END PendSV_IRQn 0 */
  /* USER CODE BEGIN PendSV_IRQn 1 */

  /* USER CODE END PendSV_IRQn 1 */
}

/**
  * @brief This function handles System tick timer.
  */
void SysTick_Handler(void)
{
  /* USER CODE BEGIN SysTick_IRQn 0 */

  /* USER CODE END SysTick_IRQn 0 */
  HAL_IncTick();
  /* USER CODE BEGIN SysTick_IRQn 1 */

  /* USER CODE END SysTick_IRQn 1 */
}

/******************************************************************************/
/* STM32L4xx Peripheral Interrupt Handlers                                    */
/* Add here the Interrupt Handlers for the used peripherals.                  */
/* For the available peripheral interrupt handler names,                      */
/* please refer to the startup file (startup_stm32l4xx.s).                    */
/******************************************************************************/

/**
  * @brief This function handles ADC1 and ADC2 interrupts.
  */
void ADC1_2_IRQHandler(void)
{
  /* USER CODE BEGIN ADC1_2_IRQn 0 */
	// Get which adc it is?
	if (__HAL_ADC_GET_FLAG(&hadc1,(ADC_FLAG_EOC | ADC_FLAG_EOS|ADC_FLAG_OVR)))
	{
		mag_hor = HAL_ADC_GetValue(&hadc1);
		__HAL_ADC_CLEAR_FLAG(&hadc1, (ADC_FLAG_EOC | ADC_FLAG_EOS|ADC_FLAG_OVR));
		adc1_new_val_flag = 1;
	}
	else if (__HAL_ADC_GET_FLAG(&hadc2,(ADC_FLAG_EOC | ADC_FLAG_EOS|ADC_FLAG_OVR)))
	{
		mag_ver = HAL_ADC_GetValue(&hadc2);
		__HAL_ADC_CLEAR_FLAG(&hadc2, (ADC_FLAG_EOC | ADC_FLAG_EOS|ADC_FLAG_OVR));
		adc2_new_val_flag = 1;
	}
  /* USER CODE END ADC1_2_IRQn 0 */
  /* USER CODE BEGIN ADC1_2_IRQn 1 */

  /* USER CODE END ADC1_2_IRQn 1 */
}

/**
  * @brief This function handles TIM3 global interrupt.
  */
void TIM3_IRQHandler(void)
{
  /* USER CODE BEGIN TIM3_IRQn 0 */
	// 0.1 ms configured maybe
	// Check if adc is running???
	//ADC_START already handled that case
	static volatile uint32_t time_counter;
	static uint32_t calib_flag = 1;
	uint32_t mag_hor_diff = 0;
	uint32_t mag_ver_diff = 0;

	time_counter++;

	if (calib_flag)
	{
		if (calib_count >= 15)
		{
			adc1_running_sum = adc1_running_sum>>15;
			adc2_running_sum = adc2_running_sum>>15;
			calib_flag = 0;
		}
		else if (adc1_new_val_flag && adc2_new_val_flag)
		{
			adc1_new_val_flag = 0;
			adc2_new_val_flag = 0;
			adc1_running_sum += mag_hor;
			adc2_running_sum += mag_ver;
			calib_count ++;
		}
	}
	else
	{
		// Basic control arch:
		// Right now turn on the coil when marble is detected, ie difference is greater than 50.
		mag_hor_diff = mag_hor>=adc1_running_sum ? mag_hor-adc1_running_sum : adc1_running_sum-mag_hor;
		mag_ver_diff = mag_ver>=adc2_running_sum ? mag_ver-adc2_running_sum : adc2_running_sum-mag_ver;
		if (mag_hor_diff > 50 || mag_ver_diff > 50)
		{
			if (mag_hor_diff > 50)
			{
				TURN_ON_COIL1();
			}
			if (mag_ver_diff > 50)
			{
				TURN_ON_COIL2();
			}
			put_data(mag_hor, mag_ver, 1);
		}
	}
	// calibration phase 16 samples.
//	if (mag_hor<3180)
//	{
//		marble_count ++ ;
//		time_counter = 0;
//		if (!marble_inside_flag)
//		{
//			marble_inside_flag = 1;
//		}
//	}
//	if (time_counter >= 1000) // give it 10ms to reset
//	{
//		time_counter = 0;
//		if (marble_inside_flag)
//		{
//			marble_inside_flag = 0;
//			marble_exit_flag = 1;
//		}
//	}
	// start ADC conversion
	HAL_ADC_Start_IT(&hadc1);
	HAL_ADC_Start_IT(&hadc2);
  /* USER CODE END TIM3_IRQn 0 */
  /* USER CODE BEGIN TIM3_IRQn 1 */
	__HAL_TIM_CLEAR_FLAG(&htim3, TIM_FLAG_UPDATE);
  /* USER CODE END TIM3_IRQn 1 */
}

/**
  * @brief This function handles USART2 global interrupt.
  */
void USART2_IRQHandler(void)
{
  /* USER CODE BEGIN USART2_IRQn 0 */
	if (__HAL_UART_GET_IT(&huart2,UART_IT_RXNE))
	{
		uint8_t RxByte=0;
		uint16_t uhMask;
		UART_MASK_COMPUTATION(&huart2);
		uhMask = huart2.Mask;
		RxByte=(uint8_t)(huart2.Instance->RDR & (uint8_t)uhMask);
		serial_data_push(RxByte);
	}
	else
	{
		// can handle more cases.
		__HAL_UART_CLEAR_IT(&huart2,UART_CLEAR_OREF);
	}
  /* USER CODE END USART2_IRQn 0 */
  /* USER CODE BEGIN USART2_IRQn 1 */

  /* USER CODE END USART2_IRQn 1 */
}

/* USER CODE BEGIN 1 */

/* USER CODE END 1 */
