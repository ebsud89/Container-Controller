FROM rabbitmq:3.11.16-management

# Add custom configuration file
COPY rabbitmq.conf /etc/rabbitmq/
COPY rabbitmq_delayed_message_exchange-3.11.1.ez /opt/rabbitmq/plugins/

# Set RabbitMQ user as the user for subsequent commands
USER rabbitmq

# Set execute permission for rabbitmq-plugins
# RUN chmod +x /usr/lib/rabbitmq/bin/rabbitmq-plugins

# Enable RabbitMQ plugins
# RUN rabbitmq-plugins enable --offline rabbitmq_management rabbitmq_delayed_message_exchange
RUN rabbitmq-plugins enable --offline rabbitmq_management
RUN rabbitmq-plugins enable --offline rabbitmq_delayed_message_exchange

# Expose ports
EXPOSE 5672 15672

# Modify RabbitMQ configuration to listen on all interfaces
# RUN echo "listeners.tcp.default = 0.0.0.0:5672" >>/etc/rabbitmq/rabbitmq.conf
# RUN echo "management.listener.port = 15672" >>/etc/rabbitmq/rabbitmq.conf
# RUN echo "management.listener.ip = 0.0.0.0" >>/etc/rabbitmq/rabbitmq.conf

# # Copy the create_users.sh script to the user's home directory
# COPY create_users.sh /home/create_users.sh
# RUN chmod +x /home/create_users.sh

# # Run the create_users.sh script during container startup
# CMD ["sh", "-c", "/home/create_users.sh && rabbitmq-server"]

# RUN rabbitmqctl add_user avadin 1thefull322
