package com.example.streamlit_integration.service;

import com.example.streamlit_integration.entity.ProductDocument;
import com.example.streamlit_integration.repository.ProductDocumentRepository;
import org.apache.poi.ss.usermodel.CellType;
import org.apache.poi.ss.usermodel.Row;
import org.apache.poi.ss.usermodel.Sheet;
import org.apache.poi.ss.usermodel.Workbook;
import org.apache.poi.xssf.usermodel.XSSFWorkbook;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.io.FileInputStream;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

@Service
public class ExcelDataService {

    @Autowired
    private ProductDocumentRepository productDocumentRepository;  // JpaRepository

    public void readExcelFile(String filePath) throws IOException {
        FileInputStream fileInputStream = new FileInputStream(filePath);
        Workbook workbook = new XSSFWorkbook(fileInputStream);
        Sheet sheet = workbook.getSheetAt(0);  // 첫 번째 시트 읽기

        List<ProductDocument> documents = new ArrayList<>();

        for (Row row : sheet) {
            ProductDocument document = new ProductDocument();

            // 인증번호 (문자열로 읽기)
            if (row.getCell(0) != null && row.getCell(0).getCellType() == CellType.STRING) {
                document.setCertificationNumber(row.getCell(0).getStringCellValue());
            }

            // 제품명 (문자열로 읽기)
            if (row.getCell(1) != null && row.getCell(1).getCellType() == CellType.STRING) {
                document.setProductName(row.getCell(1).getStringCellValue());
            }

            // 모델명 (문자열로 읽기)
            if (row.getCell(2) != null && row.getCell(2).getCellType() == CellType.STRING) {
                document.setModelName(row.getCell(2).getStringCellValue());
            }

            // V (실수로 읽기)
            if (row.getCell(3) != null && row.getCell(3).getCellType() == CellType.NUMERIC) {
                document.setVoltage(row.getCell(3).getNumericCellValue());
            }

            // A (실수로 읽기)
            if (row.getCell(4) != null && row.getCell(4).getCellType() == CellType.NUMERIC) {
                document.setCurrent(row.getCell(4).getNumericCellValue());
            }

            // URL (문자열로 읽기)
            if (row.getCell(5) != null && row.getCell(5).getCellType() == CellType.STRING) {
                document.setProductUrl(row.getCell(5).getStringCellValue());
            }

            // Image URL (문자열로 읽기)
            if (row.getCell(6) != null && row.getCell(6).getCellType() == CellType.STRING) {
                document.setImageUrl(row.getCell(6).getStringCellValue());
            }

            documents.add(document);
        }

        try {
            productDocumentRepository.saveAll(documents);
        } catch (Exception e) {
            System.out.println("데이터 저장 중 오류 발생: " + e.getMessage());
            e.printStackTrace();
        }

        workbook.close();
        fileInputStream.close();
    }}