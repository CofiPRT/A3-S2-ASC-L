// TODO
// alocati dinamic un vector vect de n elemente de tip struct particle
// verificati daca operatia a reusit
// cate elemente puteti aloca maxim (aproximativ)?
//   -> porniti de la 1.000.000 elemente; inmultiti cu 10

#include <math.h>
#include <stddef.h>
#include <stdio.h>
#include <stdint.h>     // provides int8_t, uint8_t, int16_t etc.
#include <stdlib.h>

#define ARRAY_SIZE (long)8320000000

struct particle
{
    int8_t v_x, v_y, v_z;
};

int main(int argc, char* argv[])
{
	struct particle* vect = malloc(ARRAY_SIZE * sizeof(struct particle));
	if (!vect) {
		printf("[ERROR] Could not malloc %lu particles\n", ARRAY_SIZE);
		exit(-1);
	}
	
    if(argc < 2)
    {
        printf("apelati cu %s <n>\n", argv[0]);
        return -1;
    }

    long n = atol(argv[1]);

    // generate some particles
    for(long i = 0; i < n; ++i)
    {
        vect[i].v_x = (uint8_t)rand();
        vect[i].v_y = (uint8_t)rand();
        vect[i].v_z = (uint8_t)rand();
    }

    // compute max particle speed
    float max_speed = 0.0f;
    for(long i = 0; i < n; ++i)
    {
        float speed = sqrt(vect[i].v_x * vect[i].v_x +
                           vect[i].v_y * vect[i].v_y +
                           vect[i].v_z * vect[i].v_z);
        if(max_speed < speed) max_speed = speed;
    }

    // print result
    printf("viteza maxima este: %f\n", max_speed);

    free(vect);

    return 0;
}

