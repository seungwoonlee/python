환경변수를 다음과 같이 설정함으로서 PIP 명령에서 발생하는 오류를 방지할 수 있다
```
HTTP_PROXY=http://xxx.xxx.xxx.xxx:port
HTTPS_PROXY=http://xxx.xxx.xxx.xxx:port
REQUESTS_CA_BUNDLE=C:\Users\admin\ca-cert.crt
```
ca-cert.crt 파일은 적절한 자체 인증서 파일명으로 대체
혹은
```
PYTHONHTTPSVERIFY=0
```
도 되는 것 같음 (확인 필요)
