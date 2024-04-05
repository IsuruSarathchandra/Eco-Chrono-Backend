from django.http import JsonResponse
from PIL import Image
import joblib
import numpy as np
from django.views.decorators.csrf import csrf_exempt
from keras.preprocessing.image import load_img, img_to_array
from keras.applications.imagenet_utils import preprocess_input
import numpy as np

def get_model():
    global model
    model = joblib.load('modelVGG19.pkl')


@csrf_exempt
def identify_image(request):
    get_model()
    if request.method == 'POST':
        image_file = request.FILES.get('image')
        image = Image.open(image_file)
        image = image.resize((224, 224))

        

        x = img_to_array(image)
        x = np.expand_dims(x, axis=0)
        x = preprocess_input(x)

        prediction = model.predict(x)
        predicted_class_index = np.argmax(prediction)
        class_names = ['Alstonia_scholaris','Beech','Cashew','Jackfruit','Kashid','Mango','Nilgiri','Pongamia_pinnata','Populus_tremula','Ulmus_glabra']

        # Get the class name using the predicted_class_index
        predicted_class_name = class_names[predicted_class_index]

        # Process the prediction output as needed
        response = {'Predicted class' : predicted_class_name}

        return JsonResponse(response['Predicted class'], safe=False)

    return JsonResponse({'error': 'Method not allowed'}, status=405)



