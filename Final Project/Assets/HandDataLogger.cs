using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using System.IO;
using UnityEngine.XR.Hands;
using UnityEngine.XR.Interaction.Toolkit;

public class HandDataLogger : MonoBehaviour
{
    // Start is called before the first frame update

    // private List<Vector3> handPositions = new List<Vector3>();
    public XRHand hand;
    public XRBaseInteractor leftTriggerInteractor;
    private Vector3 rightHandPosition;
    private bool isTracking;
    private string filePath;
    void Start()
    {
        leftTriggerInteractor = GetComponent<XRBaseInteractor>();

        filePath = Application.dataPath + "/hand_data.csv";

        isTracking = false;
        // if (hand == null) {
        //     Debug.LogError("Please assign a right hand XRHand object");
        // }
        
    }

    // Update is called once per frame
    void Update()
    {
        if (leftTriggerInteractor.IsActivated() && !isTracking) {
            isTracking = true;
            if (!File.Exists(filePath)) {
                File.WriteAllText(filePath, "Time,X,Y,Z\n");
            }
        } else if (leftTriggerInteractor.IsActivated() && isTracking) {
            isTracking = false;
        }


        if (isTracking) {
            // Vector3 handPosition = hand.transform.position;
            // SaveToCSV(handPosition);
            rightHandPosition = XRNodeState.GetFeaturePose(XRNode.RightHand).position;
        }
    }

    void SaveToCSV(Vector3 position) {

        return;
    }


}
