package controller;

import dto.MyData;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequestMapping("/api")
public class MyController {

    @PostMapping("/process-data")
    public ResponseEntity<String> processData(@RequestBody MyData data) {
        // 데이터를 처리한 후 응답을 반환
        String processedData = "Received: " + data.getField1() + ", " + data.getField2();
        return ResponseEntity.ok(processedData);
    }
}