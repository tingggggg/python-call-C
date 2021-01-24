#include <stdlib.h>
#include <stdio.h>

#define SWAP(x, y) {float t; t = x; x = y; y = t;}
#define SWAPINT(x, y) {int t; t = x; x = y; y = t;}
#define MAX(x, y) (x > y ? x:y)
#define MIN(x, y) (x < y ? x:y)

void BubbleSort(float *score, float* bbox, int len, int* order) 
{
	int i, j;
	for (i = 0; i < len - 1; ++i)          //循環N-1次
		for (j = 0; j < len - 1 - i; ++j)  //每次循環要比較的次數
			if (score[j] < score[j + 1])       //比大小後交換
			{
                
				SWAP(score[j], score[j + 1]);
                SWAPINT(order[j], order[j + 1]);
			}
}


int* NMS(float* bbox, float thresh, float* score, int limit, int len)
{
    int i = 0, j = 03 ;
    int *order = (int*)malloc(sizeof(int) * len);
    // init order
    for(i = 0; i < len;i++)
    {
        order[i] = i;
    }
    
    BubbleSort(score, bbox, len, order);

    // for(i = 0; i < len; i++)
    // {
    //     printf("bbox1 %f , %f, %f, %f \n", bbox[i * 4], bbox[i * 4 + 1] , bbox[i * 4 + 2], bbox[i * 4 + 3]);
    // }

    // calcu area of each bbox
    float* bbox_area = (float*)malloc(sizeof(float) * len);
    for(i = 0; i < len; i++)
    {
        int idx = i * 4;
        bbox_area[i] = (bbox[idx + 2] - bbox[idx]) * (bbox[idx + 3] - bbox[idx + 1]);
    }

    int max_conf_bbox_idxOrd, max_next_idxOrd;
    for(i = 0; i < len; i++)
    {
        if (order[i] != -1)
        {
            max_conf_bbox_idxOrd = order[i];
            for(j = i + 1; j < len; j++)
            {
                if (order[j] != -1)
                {
                    max_next_idxOrd = order[j];
                    float x11, y11, x22, y22;
                    x11 = MAX(bbox[max_conf_bbox_idxOrd * 4], bbox[max_next_idxOrd * 4]);
                    y11 = MAX(bbox[max_conf_bbox_idxOrd * 4 + 1], bbox[max_next_idxOrd * 4 + 1]);
                    x22 = MIN(bbox[max_conf_bbox_idxOrd * 4 + 2], bbox[max_next_idxOrd * 4 + 2]);
                    y22 = MIN(bbox[max_conf_bbox_idxOrd * 4 + 3], bbox[max_next_idxOrd * 4 + 3]);

                    float w = MAX(0.0, (x22 - x11));
                    float h = MAX(0.0, (y22 - y11));
                    float area = w * h;
                    float iou = area / (bbox_area[max_conf_bbox_idxOrd] + bbox_area[max_next_idxOrd] - area);

                    if(iou > thresh) 
                        order[j] = -1;
                }    
            }
        }
        
    }

    free(bbox_area);
    // free(order);
    return order;
}