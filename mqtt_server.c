#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <mosquitto.h>
//gcc mqtt_server.c -o mqtt_server -lmosquitto
#define MQTT_HOST "broker.hivemq.com"
#define MQTT_PORT 1883
#define MQTT_TOPIC "solar1"

void on_message(struct mosquitto *mosq, void *userdata, const struct mosquitto_message *message) {
    if (message->payloadlen) {
        printf("Received message: %.*s\n", message->payloadlen, (char *)message->payload);
    } else {
        printf("Empty message received\n");
    }
}

int main() {
    struct mosquitto *mosq = NULL;

    mosquitto_lib_init();

    mosq = mosquitto_new(NULL, true, NULL);
    if (!mosq) {
        fprintf(stderr, "Error: Unable to create Mosquitto instance.\n");
        return EXIT_FAILURE;
    }

    mosquitto_message_callback_set(mosq, on_message);

    if (mosquitto_connect(mosq, MQTT_HOST, MQTT_PORT, 60) != MOSQ_ERR_SUCCESS) {
        fprintf(stderr, "Error: Unable to connect to MQTT broker.\n");
        mosquitto_destroy(mosq);
        mosquitto_lib_cleanup();
        return EXIT_FAILURE;
    }

    mosquitto_subscribe(mosq, NULL, MQTT_TOPIC, 0);

    while (1) {
        mosquitto_loop(mosq, 1000, 1);  
    }

    mosquitto_disconnect(mosq);
    mosquitto_destroy(mosq);
    mosquitto_lib_cleanup();

    return EXIT_SUCCESS;
}
