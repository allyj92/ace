package com.example.streamlit_integration;

import com.example.streamlit_integration.service.ExcelDataService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.CommandLineRunner;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

@SpringBootApplication
public class StreamlitIntegrationApplication implements CommandLineRunner {

	public static void main(String[] args) {
		SpringApplication.run(StreamlitIntegrationApplication.class, args);
	}

	@Autowired
	private ExcelDataService excelDataService;

	@Override
	public void run(String... args) throws Exception {
		// 엑셀 파일 경로 설정
		String filePath = "C:\\Users\\임은재\\Desktop\\aice\\chatbot-team-prj\\streamlit-integration\\client\\codeData.xlsx";
		excelDataService.readExcelFile(filePath);
	}
}


