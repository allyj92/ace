package com.example.streamlit_integration.config;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.core.userdetails.User;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.provisioning.InMemoryUserDetailsManager;
import org.springframework.security.web.SecurityFilterChain;

@Configuration
public class WebSecurityConfig {

    @Bean
    public SecurityFilterChain securityFilterChain(HttpSecurity http) throws Exception {
        http
                .csrf().disable() // CSRF 보호를 비활성화할 경우 사용 (선택)
                .authorizeRequests()
                .antMatchers("/auth/login", "/auth/signup").permitAll() // 로그인 및 회원가입 경로 허용
                .anyRequest().authenticated() // 나머지 요청은 인증 필요
                .and()
                .formLogin()
                .loginPage("/auth/login") // 커스텀 로그인 페이지 경로
                .permitAll()
                .and()
                .logout()
                .permitAll();

        return http.build();
    }

    @Bean
    public UserDetailsService userDetailsService() {
        // 기본 사용자 생성 (테스트용)
        var user = User.withUsername("user")
                .password("{noop}password") // {noop}은 비밀번호 암호화를 생략하는 방법
                .roles("USER")
                .build();

        return new InMemoryUserDetailsManager(user);
    }
}
