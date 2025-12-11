const { createApp, reactive, ref, nextTick, onBeforeUnmount } = Vue;

createApp({
    setup() {
        // 상태 관리
        const serverUrl = ref('ws://localhost:8888/chat');
        const clientCount = ref(2);
        const clients = reactive([]);
        let clientIdCounter = 0;
        const messagesRefs = {};

        /**
         * 메시지 컨테이너 참조 설정
         */
        const setMessagesRef = (el, clientId) => {
            if (el) {
                messagesRefs[clientId] = el;
            }
        };

        /**
         * 메시지 목록 하단으로 스크롤
         */
        const scrollToBottom = (clientId) => {
            nextTick(() => {
                const el = messagesRefs[clientId];
                if (el) {
                    el.scrollTop = el.scrollHeight;
                }
            });
        };

        /**
         * 메시지 추가
         */
        const addMessage = (client, content, type = 'system') => {
            const time = new Date().toLocaleTimeString('ko-KR');
            client.messages.push({ content, type, time });
            scrollToBottom(client.id);
        };

        /**
         * 새 클라이언트 생성
         */
        const createClient = () => {
            const id = ++clientIdCounter;
            const client = reactive({
                id,
                connected: false,
                sentCount: 0,
                receivedCount: 0,
                messages: [],
                inputMessage: '',
                ws: null,
                headers: [{ key: '', value: '' }],  // 클라이언트별 커스텀 헤더
                showHeaders: false,  // 헤더 입력 영역 표시 여부
                headerTransport: 'query' // 'query' | 'protocol' | 'initmsg'
            });

            addMessage(client, `클라이언트 #${id}가 생성되었습니다. 연결 버튼을 클릭하세요.`);
            return client;
        };

        /**
         * 헤더 추가
         * @param {Object} client - 클라이언트 객체
         */
        const addHeader = (client) => {
            client.headers.push({ key: '', value: '' });
        };

        /**
         * 헤더 제거
         * @param {Object} client - 클라이언트 객체
         * @param {number} index - 제거할 헤더 인덱스
         */
        const removeHeader = (client, index) => {
            if (client.headers.length > 1) {
                client.headers.splice(index, 1);
            }
        };

        /**
         * 헤더 입력 토글
         * @param {Object} client - 클라이언트 객체
         */
        const toggleHeaders = (client) => {
            client.showHeaders = !client.showHeaders;
        };

        /**
         * 헤더 배열을 Base64 인코딩된 JSON으로 변환
         * @param {Array} headersArray - 헤더 배열 [{key, value}, ...]
         * @returns {string} Base64 인코딩된 헤더 문자열
         */
        const encodeHeadersForQuery = (headersArray) => {
            const obj = {};
            headersArray.forEach(h => {
                if (h.key && h.key.trim() !== '') {
                    obj[h.key.trim()] = h.value;
                }
            });
            if (Object.keys(obj).length === 0) return '';
            try {
                const json = JSON.stringify(obj);
                // Base64로 인코딩 (서버에서 디코드 필요)
                return btoa(unescape(encodeURIComponent(json)));
            } catch (err) {
                console.error('헤더 인코딩 실패:', err);
                return '';
            }
        };

        /**
         * 헤더를 subprotocol 용 문자열로 인코딩
         * subprotocol로 보낼 문자열 예: "ws-headers.<BASE64>"
         */
        const encodeHeadersForProtocol = (headersArray) => {
            const obj = {};
            headersArray.forEach(h => {
                if (h.key && h.key.trim() !== '') {
                    obj[h.key.trim()] = h.value;
                }
            });
            if (Object.keys(obj).length === 0) return '';
            try {
                const json = JSON.stringify(obj);
                return btoa(unescape(encodeURIComponent(json))); // Base64
            } catch (err) {
                console.error('헤더 인코딩 실패:', err);
                return '';
            }
        };

        /**
         * URL에 헤더 쿼리 파라미터 추가
         * @param {string} url - 원본 URL
         * @param {string} encodedHeaders - 인코딩된 헤더 문자열
         * @returns {string} 헤더가 추가된 URL
         */
        const appendHeadersToUrl = (url, encodedHeaders) => {
            if (!encodedHeaders) return url;
            const sep = url.includes('?') ? '&' : '?';
            return `${url}${sep}wsheaders=${encodeURIComponent(encodedHeaders)}`;
        };

        /**
         * WebSocket 연결 (수정: headerTransport 처리)
         */
        const connect = (client) => {
            if (client.ws && client.ws.readyState === WebSocket.OPEN) {
                addMessage(client, '⚠️ 이미 연결되어 있습니다.');
                return;
            }

            try {
                const encodedHeaders = encodeHeadersForQuery(client.headers);
                const protoEncoded = encodeHeadersForProtocol(client.headers);

                // 연결 방법에 따라 URL/프로토콜/초기메시지로 헤더 전송
                let urlToUse = serverUrl.value;
                let protocols = undefined;

                if (client.headerTransport === 'query') {
                    urlToUse = appendHeadersToUrl(serverUrl.value, encodedHeaders);
                } else if (client.headerTransport === 'protocol') {
                    // subprotocol에 전송: 식별 가능한 접두사를 붙여 서버에서 쉽게 파싱하도록 함
                    if (protoEncoded) {
                        protocols = [`ws-headers.${protoEncoded}`];
                    }
                } else if (client.headerTransport === 'initmsg') {
                    // URL은 그대로, 초기 메시지로 전송 (onopen에서 처리)
                }

                if (client.headerTransport === 'query' && encodedHeaders) {
                    addMessage(client, `📋 커스텀 헤더가 쿼리 파라미터로 전송됩니다.`);
                } else if (client.headerTransport === 'protocol' && protoEncoded) {
                    addMessage(client, `📋 커스텀 헤더가 서브프로토콜(Sec-WebSocket-Protocol)로 전송됩니다.`);
                } else if (client.headerTransport === 'initmsg') {
                    addMessage(client, `📋 커스텀 헤더가 연결 후 초기 메시지로 전송됩니다.`);
                }

                // WebSocket 생성 (protocols가 undefined면 생성자에 넣지 않음)
                client.ws = protocols ? new WebSocket(urlToUse, protocols) : new WebSocket(urlToUse);

                client.ws.onopen = () => {
                    addMessage(client, '✅ 서버에 연결되었습니다!');
                    client.connected = true;

                    // 초기 메시지 방식이면 첫 메시지로 헤더 전송
                    if (client.headerTransport === 'initmsg') {
                        const obj = {};
                        client.headers.forEach(h => {
                            if (h.key && h.key.trim() !== '') obj[h.key.trim()] = h.value;
                        });
                        if (Object.keys(obj).length > 0) {
                            try {
                                const initMsg = JSON.stringify(
                                    {
                                            type: 'ws_headers',
                                            payload: obj
                                        });
                                client.ws.send(initMsg);
                                addMessage(client, '📤 초기 헤더 메시지를 전송했습니다.', 'system');
                            } catch (err) {
                                addMessage(client, '❌ 초기 헤더 메시지 전송 실패: ' + err.message);
                                console.error('초기 메시지 전송 실패:', err);
                            }
                        }
                    }
                };

                client.ws.onmessage = (event) => {
                    client.receivedCount++;
                    addMessage(client, event.data, 'received');
                };

                client.ws.onerror = (error) => {
                    addMessage(client, '❌ 오류 발생: ' + (error.message || '연결 실패'));
                    console.error(`Client #${client.id} WebSocket error:`, error);
                };

                client.ws.onclose = (event) => {
                    addMessage(client, `🔌 연결이 종료되었습니다. (코드: ${event.code})`);
                    client.connected = false;
                    client.ws = null;
                };

            } catch (error) {
                addMessage(client, '❌ 연결 실패: ' + error.message);
                console.error(`Client #${client.id} connection error:`, error);
            }
        };

        /**
         * WebSocket 연결 해제
         */
        const disconnect = (client) => {
            if (client.ws && client.ws.readyState === WebSocket.OPEN) {
                client.ws.close();
                addMessage(client, '👋 연결을 종료합니다...');
            }
        };

        /**
         * 메시지 전송
         */
        const sendMessage = (client) => {
            const message = client.inputMessage.trim();

            if (!message) return;

            if (!client.ws || client.ws.readyState !== WebSocket.OPEN) {
                addMessage(client, '❌ 서버에 연결되어 있지 않습니다.');
                return;
            }

            try {
                client.ws.send(message);
                client.sentCount++;
                addMessage(client, message, 'sent');
                client.inputMessage = '';
            } catch (error) {
                addMessage(client, '❌ 메시지 전송 실패: ' + error.message);
                console.error(`Client #${client.id} send error:`, error);
            }
        };

        /**
         * 여러 클라이언트 생성
         */
        const createClients = () => {
            if (!serverUrl.value) {
                alert('서버 URL을 입력해주세요.');
                return;
            }

            if (clientCount.value < 1 || clientCount.value > 10) {
                alert('클라이언트 수는 1~10 사이여야 합니다.');
                return;
            }

            for (let i = 0; i < clientCount.value; i++) {
                clients.push(createClient());
            }
        };

        /**
         * 특정 클라이언트 제거
         */
        const removeClient = (id) => {
            const index = clients.findIndex(c => c.id === id);
            if (index !== -1) {
                const client = clients[index];
                if (client.ws) {
                    client.ws.close();
                }
                delete messagesRefs[id];
                clients.splice(index, 1);
            }
        };
        /**
         * 모든 클라이언트 연결
         */
        const connectAll = () => {
            clients.forEach(client => connect(client));
        };
        /**
         * 모든 클라이언트 연결 해제
         */
        const disconnectAll = () => {
            clients.forEach(client => disconnect(client));
        };

        /**
         * 모든 클라이언트 제거
         */
        const removeAllClients = () => {
            clients.forEach(client => {
                if (client.ws) {
                    client.ws.close();
                }
            });
            clients.splice(0, clients.length);
            clientIdCounter = 0;
        };

        // 생명주기: 컴포넌트 언마운트 전 정리
        onBeforeUnmount(() => {
            disconnectAll();
        });

        // 초기 클라이언트 생성
        nextTick(() => {
            createClients();
        });

        // 템플릿에 노출할 API
        return {
            serverUrl,
            clientCount,
            clients,
            setMessagesRef,
            connect,
            disconnect,
            sendMessage,
            createClients,
            removeClient,
            connectAll,
            disconnectAll,
            removeAllClients,
            addHeader,
            removeHeader,
            toggleHeaders
        };
    }
}).mount('#app');