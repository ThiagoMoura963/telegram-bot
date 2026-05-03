# type: ignore


class ConversationService:
    def __init__(self, message_repository, chunk_repository, chat_service):
        self.message_repository = message_repository
        self.chunk_repository = chunk_repository
        self.chat_service = chat_service

    def execute_chat_flow(self, user_id, agent_id, text, system_prompt):
        query_vector = self.chat_service.get_query_vector(text)

        docs = self.chunk_repository.find_similiar_chunk(query_vector, limit=10, agent_id=agent_id)
        semantic_memory = self.message_repository.search_semantic_history(user_id, agent_id, query_vector, limit=3)

        linear_history = self.message_repository.get_history(user_id, agent_id, limit=1)

        final_system_instruction = self._build_prompt(base_prompt=system_prompt, docs=docs, memory=semantic_memory)

        answer = self.chat_service.get_answer(
            message=text, system_instruction=final_system_instruction, history=linear_history
        )

        self.message_repository.save(user_id, agent_id, 'user', text, None)
        self.message_repository.save(user_id, agent_id, 'model', answer, None)

        return answer

    def _build_prompt(self, base_prompt, docs, memory):
        if docs:
            docs_list = []
            for d in docs:
                source = d.get('metadata', {}).get('source') or d.get('source') or 'Documento Técnico'
                content = d.get('content', '').strip()
                docs_list.append(f'FONTE: {source}\nTRECHO: {content}')
            docs_section = '\n\n'.join(docs_list)
        else:
            docs_section = 'Nenhuma informação técnica encontrada nos documentos oficiais.'

        memory_section = '\n'.join([f'- {m["content"]}' for m in memory]) if memory else 'Nenhuma lembrança relevante.'

        return f"""
            {base_prompt}

            ### BASE DE CONHECIMENTO OFICIAL (RAG)
            Você deve priorizar as informações abaixo. Sempre que usar um dado desta seção, cite explicitamente o 
            nome da fonte.
            {docs_section}

            ### MEMÓRIA SEMÂNTICA (Fatos registrados pelo usuário)
            Estes são fatos que o usuário te ensinou anteriormente via comando /registrar:
            {memory_section}

            ---
            ### DIRETRIZES DE RESPOSTA:
            1. Se a informação vier da 'BASE DE CONHECIMENTO', cite a fonte: "Segundo o documento [nome]...".
            2. Se a informação vier da 'MEMÓRIA SEMÂNTICA', trate como algo que o usuário já te contou.
            3. Se o usuário perguntar quais documentos você possui, liste as FONTES citadas acima.
            4. Utilize MarkdownV2 para a formatação no Telegram.
        """
