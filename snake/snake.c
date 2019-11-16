#include<stdio.h>                       /* ALLEGRO SNAKE                              */
#include<stdlib.h>                      /* Made by Lorand Horvath 2016                */
#include<time.h>                        /* Controls: Up, Down, Left, Right            */
#include<allegro5/allegro.h>            /* Gameplay video:                            */
#include<allegro5/allegro_primitives.h> /* https://gfycat.com/assuredmarriedarmadillo */

int main(){
    // screen init
    al_init();
    al_init_primitives_addon();
    ALLEGRO_DISPLAY* display;
    display = al_create_display(600,600);

    // keyboard and event queue init
    al_install_keyboard();
    ALLEGRO_EVENT_QUEUE* eq = al_create_event_queue();
    al_register_event_source(eq, al_get_keyboard_event_source());
    ALLEGRO_EVENT ev;

    // timer init
    ALLEGRO_TIMER* tim = al_create_timer(0.5); printf("speed: 50\n");
    al_register_event_source(eq, al_get_timer_event_source(tim));
    al_start_timer(tim); srand(time(NULL));
//-----------------------------------------------------------------------
int body_x[100] = {0};  // body coordinates
int body_y[100] = {0};
body_x[0] = 5;          // initial head position
body_y[0] = 5;
int food_x = 2;         // first food position
int food_y = 2;
int length = 2;         // initial length
int direction = 0;      // initial direction
int i;          // loop variable
int end = 0;    // game ended?

/* ######################## GAMELOOP ######################## */
while(1){
    al_wait_for_event(eq,&ev);

    /**************** MOVE ****************/
    if (ev.type == ALLEGRO_EVENT_KEY_DOWN){
        switch(ev.keyboard.keycode){
            case ALLEGRO_KEY_UP:    direction = 0; break;
            case ALLEGRO_KEY_RIGHT: direction = 1; break;
            case ALLEGRO_KEY_DOWN:  direction = 2; break;
            case ALLEGRO_KEY_LEFT:  direction = 3; break;
        }
    }
    if (ev.type == ALLEGRO_EVENT_TIMER){
        // move whole body
        for(i=length; i>=1; i--){
            body_x[i] = body_x[i-1];
            body_y[i] = body_y[i-1];
        }
        // move head to the new direction
        switch(direction){
            case 0: body_y[0] = body_y[0]-1; break; //eszak
            case 1: body_x[0] = body_x[0]+1; break; //kelet
            case 2: body_y[0] = body_y[0]+1; break; //del
            case 3: body_x[0] = body_x[0]-1; break; //nyugat
        }
        /**************** CHECK RULES ****************/
        // check if we hit our body
        for(i=1; i<length; i++){
            if(body_x[0] == body_x[i]   &&   body_y[0] == body_y[i]){
                end = 1;
            }
        }
        // check if we hit playground edges
        if(body_x[0] < 0 || body_y[0] <0 || body_x[0] > 9 || body_y[0] > 9){
            end = 1;
        }
        // game ended
        if(end){
            al_clear_to_color(al_map_rgb(255,0,0));
            al_flip_display(); printf("end\n");
            al_rest(5); return 0;
        }
        /**************** DRAW ****************/
        al_clear_to_color(al_map_rgb(0,0,0));
        al_draw_filled_rectangle(food_x*60, food_y*60, food_x*60+60, food_y*60+60, al_map_rgb(0,255,0));                // food
        al_draw_filled_rectangle(body_x[0]*60, body_y[0]*60, body_x[0]*60+60, body_y[0]*60+60, al_map_rgb(255,0,0));    // head
        for(i=1; i<length; i++){
            al_draw_filled_rectangle(body_x[i]*60, body_y[i]*60, body_x[i]*60+60, body_y[i]*60+60, al_map_rgb(0,0,255));// body
        }
        /**************** EAT FOOD ****************/
        if(body_x[0] == food_x && body_y[0] == food_y){
            length++;   printf("length: %d\n",length);
            food_x = rand()%10;
            food_y = rand()%10;
        }
        // speed up
        if(length == 5){  al_set_timer_speed(tim,0.3);  printf("speed: 70\n"); }
        if(length == 10){  al_set_timer_speed(tim,0.2); printf("speed: 80\n");  }
    al_flip_display();
    }
}

return 0;
}
