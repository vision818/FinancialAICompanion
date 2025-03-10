if st.button("Ask"):
        with st.spinner("Thinking..."):
            try:
                response = get_ai_response(user_input)

                # Save chat to database
                with get_session() as db:
                    chat = ChatHistory(question=user_input, answer=response)
                    db.add(chat)
                    db.commit()

                st.session_state.chat_history.append({"question": user_input, "answer": response})
            except Exception as e:
                st.error(f"Error getting AI response: {str(e)}")

    # Display chat history from database
    with get_session() as db:
        chats = db.query(ChatHistory).order_by(ChatHistory.timestamp.desc()).limit(5).all()
        for chat in chats:
            st.markdown("---")
            st.markdown("**You:** " + chat.question)
            st.markdown("**AI:** " + chat.answer)