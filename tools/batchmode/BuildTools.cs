using UnityEditor;
using UnityEngine;
using System.Collections.Generic;
using UnityEditor.Purchasing;
using UnityEngine.Purchasing;

public class BuildTools
{
    static string apkPath = null;

    static void Init()
    {
        string[] args = System.Environment.GetCommandLineArgs();
        for (int i = 0; i < args.Length; i++)
        {
            switch (args[i])
            {
                case "-packageName":
                    PlayerSettings.applicationIdentifier = args[++i];
                    break;
                case "-iapTarget":
                    AppStore appStore = AppStore.GooglePlay;
                    switch (args[++i])
                    {
                        case "Xiaomi":
                            appStore = AppStore.XiaomiMiPay;
                            break;
                        case "GooglePlay":
                            appStore = AppStore.GooglePlay;
                            break;
                        case "Amazon":
                            appStore = AppStore.AmazonAppStore;
                            break;
                        case "CloudMoolah":
                            appStore = AppStore.CloudMoolah;
                            break;
                        case "Samsung":
                            appStore = AppStore.SamsungApps;
                            break;
                    }
                    UnityPurchasingEditor.TargetAndroidStore(appStore);
                    break;
                case "-apkPath":
                    apkPath = args[++i];
                    break;
                case "-keystoreName":
                    PlayerSettings.Android.keystoreName = args[++i];
                    break;
                case "-keystorePass":
                    PlayerSettings.Android.keystorePass = args[++i];
                    break;
                case "-keyaliasName":
                    PlayerSettings.Android.keyaliasName = args[++i];
                    break;
                case "-keyaliasPass":
                    PlayerSettings.Android.keyaliasPass = args[++i];
                    break;
                case "-productName":
                    PlayerSettings.productName = args[++i];
                    break;
                default:
                    break;
            }
        }
    }

    static string[] GetBuildScenes()
    {
        List<string> scenes = new List<string>();
        foreach (EditorBuildSettingsScene scene in EditorBuildSettings.scenes)
        {
            if (scene != null && scene.enabled)
                scenes.Add(scene.path);
        }
        return scenes.ToArray();
    }

    static void Build4Android()
    {
        Init();
        string[] scenes = new string[] { "Assets/Plugins/UnityPurchasing/scenes/IAP Demo.unity" };
        string result = BuildPipeline.BuildPlayer(scenes, apkPath, BuildTarget.Android, BuildOptions.None);
        Debug.Log("Build result: " + result);
    }
}
