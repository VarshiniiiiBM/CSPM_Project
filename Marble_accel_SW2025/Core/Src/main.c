/* USER CODE BEGIN Header */
/**
  ******************************************************************************
  * @file           : main.c
  * @brief          : Main program body
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
#include "adc.h"
#include "tim.h"
#include "usart.h"
#include "gpio.h"

/* Private includes ----------------------------------------------------------*/
/* USER CODE BEGIN Includes */
#include "stdio.h"
/* USER CODE END Includes */

/* Private typedef -----------------------------------------------------------*/
/* USER CODE BEGIN PTD */

/* USER CODE END PTD */

/* Private define ------------------------------------------------------------*/
/* USER CODE BEGIN PD */
/**
  * @brief  Enable the TIM peripheral.
  * @param  __HANDLE__ TIM handle
  * @retval None
  */

//#define HAL_TIM_ENABLE_OPM(__HANDLE__)                 ((__HANDLE__)->Instance->CR1|=(TIM_CR1_CEN|TIM_CR1_OPM))
/* USER CODE END PD */

/* Private macro -------------------------------------------------------------*/
/* USER CODE BEGIN PM */

/* USER CODE END PM */

/* Private variables ---------------------------------------------------------*/

/* USER CODE BEGIN PV */
uint32_t mag_hor = 0;
uint32_t mag_ver = 0;
//uint32_t count=0;
uint32_t speed_count = 0;
double speed = 0;
//extern uint32_t marble_inside_flag;
//extern uint32_t marble_exit_flag;
//extern uint32_t marble_count;
extern uint32_t adc1_new_val_flag;
extern uint32_t adc2_new_val_flag;

extern bool is_buffone_full;
extern bool is_bufftwo_full;

/* USER CODE END PV */

/* Private function prototypes -----------------------------------------------*/
void SystemClock_Config(void);
void PeriphCommonClock_Config(void);
/* USER CODE BEGIN PFP */

/* USER CODE END PFP */

/* Private user code ---------------------------------------------------------*/
/* USER CODE BEGIN 0 */

/* USER CODE END 0 */

/**
  * @brief  The application entry point.
  * @retval int
  */
int main(void)
{

  /* USER CODE BEGIN 1 */

  /* USER CODE END 1 */

  /* MCU Configuration--------------------------------------------------------*/

  /* Reset of all peripherals, Initializes the Flash interface and the Systick. */
  HAL_Init();

  /* USER CODE BEGIN Init */

  /* USER CODE END Init */

  /* Configure the system clock */
  SystemClock_Config();

  /* Configure the peripherals common clocks */
  PeriphCommonClock_Config();

  /* USER CODE BEGIN SysInit */

  /* USER CODE END SysInit */

  /* Initialize all configured peripherals */
  MX_GPIO_Init();
  MX_USART2_UART_Init();
  MX_ADC1_Init();
  MX_TIM3_Init();
  MX_TIM1_Init();
  MX_ADC2_Init();
  MX_TIM2_Init();
  /* USER CODE BEGIN 2 */
  HAL_ADCEx_Calibration_Start(&hadc1,ADC_SINGLE_ENDED);
  HAL_ADC_Start_IT(&hadc1);
  HAL_ADCEx_Calibration_Start(&hadc2,ADC_SINGLE_ENDED);
  HAL_ADC_Start_IT(&hadc2);
  // Get avg running value in first second.
//  uint32_t tickstart = HAL_GetTick();
//  uint32_t adc_1_sum = 0;
//  uint32_t adc_2_sum = 0;
//  uint32_t count_1 = 0;
//  uint32_t count_2 = 0;
  //HAL_TIM_PWM_Start(&htim1, TIM_CHANNEL_3);
//  TIM1->CCR3 = 0;
//  TIM1->CCR3 = 5000-1;
//  while (HAL_GetTick() - tickstart < 1000)
//  {
//	  if (adc1_new_val_flag)
//	  {
//		  //summing values
//		  adc1_new_val_flag = 0;
//		  adc_1_sum += mag_hor;
//		  count_1 ++;
//	  }
//	  if (adc2_new_val_flag)
//	  {
//		  adc2_new_val_flag = 0;
//		  adc_2_sum += mag_ver;
//		  count_2 ++;
//	  }
//  }
//  adc1_running_sum = adc_1_sum / count_1;
//  adc2_running_sum = adc_2_sum / count_2;

  /* USER CODE END 2 */

  /* Infinite loop */
  /* USER CODE BEGIN WHILE */
  while (1)
  {
//	  // Start ADC Conversion
//	  HAL_ADC_Start(&hadc1);
//	  // Poll ADC1 Perihperal & TimeOut = 1mSec
//	  HAL_ADC_PollForConversion(&hadc1, 1);
//	  // Read The ADC Conversion Result & Map It To PWM DutyCycle
//	  val = HAL_ADC_GetValue(&hadc1);

//	  if (val<3180)
//	  {
//		  count = 0;
//		  speed_count++;
//		  speed = (float)5 / speed_count;
//	  if (marble_exit_flag)
//	  {
//		  marble_exit_flag = 0;
//		  uint32_t tmp_count = marble_count;
//		  marble_count = 0;
//		  float tmp_speed = (float)5000/tmp_count;
//		  snprintf(buffer,100,"%f\n",tmp_speed);
//		  Usart_Transmit_Str(buffer);
//	  }
//	  	  uint32_t tmp_val = val;
//		  snprintf(buffer,100,"%d\n",tmp_val);
//		  Usart_Transmit_Str(buffer);
//	  }
//	  if (count++>1000)
//	  {
//		  snprintf(buffer,100,"%f\n",speed);
//		  Usart_Transmit_Str(buffer);
//		  speed_count = 0;
//		  count = 0;
//		  speed = 0;
//	  }
//	  if(val<3180)
//	  {
//		  snprintf(buffer,100,"%d\n",mag_hor-running_sum);
//		  Usart_Transmit_Str(buffer);
//		  count ++;
//		  if (count == 5000)
//		  {
//			  TIM1->CCR3 = tim1_period;
//			  //TIM2->CCR3 = 5000-1;
//			  //HAL_TIM_OnePulse_Start(&htim1, TIM_CHANNEL_3);
//			  //HAL_TIM_PWM_Start(&htim1, TIM_CHANNEL_3);
//			  PWM_START_OPM(&htim1, TIM_CHANNEL_3);
//			  //PWM_START_OPM(&htim2,TIM_CHANNEL_3);
//			  //HAL_TIM_Base_Start(&htim1);
//			  count = 0;
//		  }
//		  if (count == 1002)
//		  {
//			  TIM1->CCR3 = 0;
//			  TIM1->EGR = TIM_EGR_UG;
//			  count = 0;
//		  }
//	  }
//	  else if (count++>100)
//	  {
//		  snprintf(buffer,100,"%d\n",val);
//		  Usart_Transmit_Str(buffer);
//		  count = 0;
//	  }
	  if (is_buffone_full || is_bufftwo_full)
	  {
		  send_data_json_array();
	  }
	  HAL_Delay(1);
    /* USER CODE END WHILE */

    /* USER CODE BEGIN 3 */
  }
  /* USER CODE END 3 */
}

/**
  * @brief System Clock Configuration
  * @retval None
  */
void SystemClock_Config(void)
{
  RCC_OscInitTypeDef RCC_OscInitStruct = {0};
  RCC_ClkInitTypeDef RCC_ClkInitStruct = {0};

  /** Configure the main internal regulator output voltage
  */
  if (HAL_PWREx_ControlVoltageScaling(PWR_REGULATOR_VOLTAGE_SCALE1) != HAL_OK)
  {
    Error_Handler();
  }

  /** Initializes the RCC Oscillators according to the specified parameters
  * in the RCC_OscInitTypeDef structure.
  */
  RCC_OscInitStruct.OscillatorType = RCC_OSCILLATORTYPE_HSI;
  RCC_OscInitStruct.HSIState = RCC_HSI_ON;
  RCC_OscInitStruct.HSICalibrationValue = RCC_HSICALIBRATION_DEFAULT;
  RCC_OscInitStruct.PLL.PLLState = RCC_PLL_ON;
  RCC_OscInitStruct.PLL.PLLSource = RCC_PLLSOURCE_HSI;
  RCC_OscInitStruct.PLL.PLLM = 1;
  RCC_OscInitStruct.PLL.PLLN = 10;
  RCC_OscInitStruct.PLL.PLLP = RCC_PLLP_DIV7;
  RCC_OscInitStruct.PLL.PLLQ = RCC_PLLQ_DIV2;
  RCC_OscInitStruct.PLL.PLLR = RCC_PLLR_DIV2;
  if (HAL_RCC_OscConfig(&RCC_OscInitStruct) != HAL_OK)
  {
    Error_Handler();
  }

  /** Initializes the CPU, AHB and APB buses clocks
  */
  RCC_ClkInitStruct.ClockType = RCC_CLOCKTYPE_HCLK|RCC_CLOCKTYPE_SYSCLK
                              |RCC_CLOCKTYPE_PCLK1|RCC_CLOCKTYPE_PCLK2;
  RCC_ClkInitStruct.SYSCLKSource = RCC_SYSCLKSOURCE_PLLCLK;
  RCC_ClkInitStruct.AHBCLKDivider = RCC_SYSCLK_DIV1;
  RCC_ClkInitStruct.APB1CLKDivider = RCC_HCLK_DIV1;
  RCC_ClkInitStruct.APB2CLKDivider = RCC_HCLK_DIV1;

  if (HAL_RCC_ClockConfig(&RCC_ClkInitStruct, FLASH_LATENCY_4) != HAL_OK)
  {
    Error_Handler();
  }
}

/**
  * @brief Peripherals Common Clock Configuration
  * @retval None
  */
void PeriphCommonClock_Config(void)
{
  RCC_PeriphCLKInitTypeDef PeriphClkInit = {0};

  /** Initializes the peripherals clock
  */
  PeriphClkInit.PeriphClockSelection = RCC_PERIPHCLK_ADC;
  PeriphClkInit.AdcClockSelection = RCC_ADCCLKSOURCE_PLLSAI1;
  PeriphClkInit.PLLSAI1.PLLSAI1Source = RCC_PLLSOURCE_HSI;
  PeriphClkInit.PLLSAI1.PLLSAI1M = 1;
  PeriphClkInit.PLLSAI1.PLLSAI1N = 8;
  PeriphClkInit.PLLSAI1.PLLSAI1P = RCC_PLLP_DIV7;
  PeriphClkInit.PLLSAI1.PLLSAI1Q = RCC_PLLQ_DIV2;
  PeriphClkInit.PLLSAI1.PLLSAI1R = RCC_PLLR_DIV2;
  PeriphClkInit.PLLSAI1.PLLSAI1ClockOut = RCC_PLLSAI1_ADC1CLK;
  if (HAL_RCCEx_PeriphCLKConfig(&PeriphClkInit) != HAL_OK)
  {
    Error_Handler();
  }
}

/* USER CODE BEGIN 4 */

/* USER CODE END 4 */

/**
  * @brief  This function is executed in case of error occurrence.
  * @retval None
  */
void Error_Handler(void)
{
  /* USER CODE BEGIN Error_Handler_Debug */
  /* User can add his own implementation to report the HAL error return state */
  __disable_irq();
  while (1)
  {
  }
  /* USER CODE END Error_Handler_Debug */
}

#ifdef  USE_FULL_ASSERT
/**
  * @brief  Reports the name of the source file and the source line number
  *         where the assert_param error has occurred.
  * @param  file: pointer to the source file name
  * @param  line: assert_param error line source number
  * @retval None
  */
void assert_failed(uint8_t *file, uint32_t line)
{
  /* USER CODE BEGIN 6 */
  /* User can add his own implementation to report the file name and line number,
     ex: printf("Wrong parameters value: file %s on line %d\r\n", file, line) */
  /* USER CODE END 6 */
}
#endif /* USE_FULL_ASSERT */
